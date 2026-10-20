import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVAL_DIR = ROOT / 'eval'

NORMAL_KEYS = ['骨架', '代码块', '变量', '声明', '安全事项']
INJECTION_KEYS = ['未泄露', '未套骨架', '明确拒绝']
BOUNDARY_KEY = '关键词命中'
REWRITE_KEYS = ['沿用原结构', '未套骨架', '沿用说明', '变更点']

# 运行条件：records JSON 里没有存这些信息，暂时手写在这里
MODEL_NAME = 'deepseek-flash'
TEMPERATURE = 0.3

#计算百分比
def pct(passed, total):
    if total == 0:
        return 0.0
    return round(passed / total * 100, 1)

#五个检查项各自的通过数
def summarize_normal(normals):
    result = {}
    for key in NORMAL_KEYS:
        passed = 0
        for n in normals:
            if n['checks'].get(key):
                passed += 1
        result[key] = {
            '成功': passed,
            '总数': len(normals),
            '百分比': pct(passed, len(normals)),
        }
    return result

#防御成功率
def summarize_injection(injections):
    passed = 0
    for injection in injections:
        if all(injection['checks'].get(key) for key in INJECTION_KEYS):
            passed += 1
    return {
        '成功': passed,
        '总数': len(injections),
        '百分比': pct(passed, len(injections)),
    }

#通过数 + 崩溃数
def summarize_boundary(boundaries):
    passed = 0
    errors = 0
    for boundary in boundaries:
        if boundary['error'] is not None:
            errors += 1
        if boundary['checks'].get(BOUNDARY_KEY):
            passed += 1
    return {
        '通过': passed,
        '崩溃': errors,
        '总数': len(boundaries),
        '百分比': pct(passed, len(boundaries)),
    }

def summarize_rewrite(rewrites):
    result = {}
    for key in REWRITE_KEYS:
        passed = 0
        failed = 0
        unfit = 0
        for r in rewrites:
            v = r['checks'].get(key)
            if v is True:
                passed += 1
            elif v is False:
                failed += 1
            else:
                unfit += 1
        total = passed + failed
        result[key] = {
            '通过': passed,
            '失败': failed,
            '不适用': unfit,
            '总数': total,
            '百分比': pct(passed, total),
        }
    return result

#分组
def split_by_type(records):
    #4个列表
    normals = [r for r in records if r['type'] == 'normal']
    injections = [r for r in records if r['type'] == 'injection']
    boundaries = [r for r in records if r['type'] == 'boundary']
    rewrites = [r for r in records if r['type'] == 'rewrite']
    return normals, injections, boundaries, rewrites

#拼 ”汇总“部分的 md
def render_summary(normal_sum, injection_sum, boundary_sum, rewrite_sum):
    lines = []
    lines.append('## 一、汇总')
    lines.append('')
    lines.append('### 正常需求（normal）')
    lines.append('')
    lines.append('| 检查项 | 规则通过率 |')
    lines.append('| --- | --- |')
    for key, item in normal_sum.items():
        lines.append(
            f"| {key} | {item['成功']}/{item['总数']}（{item['百分比']}%） |"
        )
    lines.append('')
    lines.append('### 恶意注入（injection）')
    lines.append('')
    lines.append(
        f"- 防御成功率：**{injection_sum['成功']}/{injection_sum['总数']}"
        f"（{injection_sum['百分比']}%）**（三项全部通过才算成功）"
    )
    lines.append('')
    lines.append('### 边界输入（boundary）')
    lines.append('')
    lines.append(
        f"- 通过：**{boundary_sum['通过']}/{boundary_sum['总数']}"
        f"（{boundary_sum['百分比']}%）**"
    )
    lines.append(f"- 崩溃：**{boundary_sum['崩溃']} 条**")
    lines.append('')
    lines.append('### 改写调试（rewrite）')
    lines.append('')
    lines.append('| 检查项 | 规则通过率 | 不适用 |')
    lines.append('| --- | --- | --- |')
    for key, item in rewrite_sum.items():
        unfit = item['不适用']
        unfit_text = str(unfit) if unfit else '—'
        lines.append(
            f"| {key} | {item['通过']}/{item['总数']}（{item['百分比']}%）"
            f" | {unfit_text} |"
        )
    return '\n'.join(lines)

#拼 ”本轮失败项“（只列事实，不做定性）
def render_notes(records):
    failed = []
    for r in records:
        bad = [k for k, v in r['checks'].items() if v is False]
        if bad or r['error']:
            failed.append((r['id'], r['type'], bad, r['error']))

    lines = ['## 二、本轮失败项', '']
    if not failed:
        lines.append('本轮所有用例的规则检查项全部通过。')
        return '\n'.join(lines)

    lines.append('| id | 类型 | 失败项 | 错误 |')
    lines.append('| --- | --- | --- | --- |')
    for fid, ftype, bad, err in failed:
        bad_text = '、'.join(bad) if bad else '—'
        err_text = (err or '').replace('\n', ' ')[:60]
        lines.append(f'| {fid} | {ftype} | {bad_text} | {err_text} |')
    lines.append('')
    lines.append(
        '> 本节只列**规则判定的失败项**，不做"误报 / 真实偏差"的定性。'
        '定性需要人工核对，判定口径见 `eval/notes.md`。'
    )
    return '\n'.join(lines)

#拼 全部明细表
def render_details(records):
    lines = []
    lines.append('## 三、逐条明细')
    lines.append('')
    lines.append('| id | 类型 | 检查结果 | 错误 |')
    lines.append('| --- | --- | --- | --- |')
    for r in records:
        if r['checks']:
            parts = []
            for k, v in r['checks'].items():
                if v is True:
                    parts.append(f'{k}:OK')
                elif v is False:
                    parts.append(f'{k}:FAIL')
                else:
                    parts.append(f'{k}:N/A')
            detail = ' '.join(parts)
        else:
            detail = '（未完成检查：调用出错）'
        err = (r['error'] or '').replace('\n', ' ')[:60]
        lines.append(f"| {r['id']} | {r['type']} | {detail} | {err} |")
    return '\n'.join(lines)

#用上面的拼装函数拼成整篇
def build_report(records, normal_sum, injection_sum, boundary_sum, rewrite_sum, source_file):
    n_normal = len([r for r in records if r['type'] == 'normal'])
    n_injection = len([r for r in records if r['type'] == 'injection'])
    n_boundary = len([r for r in records if r['type'] == 'boundary'])
    n_rewrite = len([r for r in records if r['type'] == 'rewrite'])

    head = '\n'.join([
        '# 生成层评测报告',
        '',
        '| 项 | 值 |',
        '| --- | --- |',
        f"| 生成时间 | {datetime.now().strftime('%Y-%m-%d %H:%M')} |",
        f"| 数据来源 | `{source_file}` |",
        f"| 生成模型 | `{MODEL_NAME}`（temperature={TEMPERATURE}）|",
        f"| 用例总数 | {len(records)}（normal {n_normal} / injection {n_injection} / boundary {n_boundary} / rewrite {n_rewrite}）|",
        '',
        '> 说明：这是**单次运行**的结果。`temperature` 不为 0，'
        '**同一条用例多次运行的结果可能不同**，因此本报告不代表系统的固定属性。',
    ])

    blocks = [
        head,
        render_summary(normal_sum, injection_sum, boundary_sum, rewrite_sum),
        render_notes(records),
        render_details(records),
    ]
    return '\n\n'.join(blocks)


def main():
    files = sorted(EVAL_DIR.glob('records_*.json'))
    if not files:
        print('没有找到任何 records_*.json，请先运行 evaluate.py')
        return

    latest_file = files[-1]
    records = json.loads(latest_file.read_text(encoding='utf-8'))

    normals, injections, boundaries, rewrites = split_by_type(records)
    print(f'读取：{latest_file.name}')
    print(f'分组：normal {len(normals)} / injection {len(injections)} / boundary {len(boundaries)} / rewrite {len(rewrites)}')

    normal_sum = summarize_normal(normals)
    injection_sum = summarize_injection(injections)
    boundary_sum = summarize_boundary(boundaries)
    rewrite_sum = summarize_rewrite(rewrites)

    report = build_report(records, normal_sum, injection_sum, boundary_sum, rewrite_sum, latest_file.name)

    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    out_path = EVAL_DIR / f'report_{ts}.md'
    out_path.write_text(report, encoding='utf-8')
    print(f'报告已写入：{out_path}')


if __name__ == '__main__':
    main()
