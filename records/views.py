from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F, Q
from .models import AnomalyRecord, PlayerJudgement
from .forms import JudgementForm

# ==============================
# スタート画面
# ==============================
def start_view(request):
    return render(request, "records/start.html")

def start_game(request):
    PlayerJudgement.objects.all().delete()
    first_record = AnomalyRecord.objects.order_by("id").first()
    return redirect("records:detail", pk=first_record.pk)


# ==============================
# 記録一覧
# ==============================
def record_list(request):
    records = AnomalyRecord.objects.all().order_by('-observed_at')

    judged_ids = set(
        PlayerJudgement.objects.values_list("record_id", flat=True)
    )

    return render(request, "records/record_list.html", {
        "records": records,
        "judged_ids": judged_ids,
    })

# ==============================
# 記録詳細 + 判定
# ==============================
def record_detail(request, pk):
    record = get_object_or_404(AnomalyRecord, pk=pk)
    judgement = PlayerJudgement.objects.filter(record=record).first()
    warning = False

    if judgement and abs(judgement.judgement - record.anomaly_level) >= 2:
        warning = True

    if request.method == "POST" and not judgement:
        form = JudgementForm(request.POST)
        if form.is_valid():
            new_judgement = form.save(commit=False)
            new_judgement.record = record
            new_judgement.save()

            # 次の未判定レコードへ
            next_record = AnomalyRecord.objects.exclude(
                judgements__isnull=False
            ).first()

            if next_record:
                return redirect("records:detail", pk=next_record.pk)
            else:
                return redirect("records:analysis")
    else:
        form = None if judgement else JudgementForm()

    return render(request, "records/record_detail.html", {
        "record": record,
        "form": form,
        "judgement": judgement,
        "warning": warning,
    })


# ==============================
# 分析ページ（★ここが今回の本命）
# ==============================
def analysis_view(request):
    judgements = PlayerJudgement.objects.select_related('record')
    total = judgements.count()

    correct = judgements.filter(
        judgement=F('record__anomaly_level')
    ).count()

    one_step_diff = judgements.filter(
        Q(judgement=F('record__anomaly_level') + 1) |
        Q(judgement=F('record__anomaly_level') - 1)
    ).count()

    major_diff = total - correct - one_step_diff

    # ==============================
    # 乖離率 & 正確率
    # ==============================
    if total > 0:
        deviation_rate = int((major_diff / total) * 100)
        accuracy = correct / total
    else:
        deviation_rate = 0
        accuracy = 0

    # ==============================
    # 警告レベル（量）
    # ==============================
    if deviation_rate < 20:
        warning_level = "mild"
    elif deviation_rate < 40:
        warning_level = "medium"
    else:
        warning_level = "severe"

    # ==============================
    # 判断傾向（質）
    # ==============================
    if accuracy >= 0.8:
        warning_type = "overfit"      # 合いすぎている
    elif major_diff >= total * 0.4:
        warning_type = "divergent"    # ズレすぎ
    else:
        warning_type = "uncertain"    # 判別不能

    # ==============================
    # 異常度ごとの一致率
    # ==============================
    level_stats_list = []
    for level in [1, 2, 3, 4, 5]:
        total_level = PlayerJudgement.objects.filter(
            record__anomaly_level=level
        ).count()

        correct_level = PlayerJudgement.objects.filter(
            record__anomaly_level=level,
            judgement=F('record__anomaly_level')
        ).count()

        percent = int(correct_level / total_level * 100) if total_level > 0 else 0

        level_stats_list.append({
            "level": level,
            "percent": percent
        })

    # ==============================
    # 異常度ごとの型判定（乖離率による）
    # ==============================
    # 判定タイプと型説明
    type_descriptions = {
        "慎重観測型": "異常を過小評価せず、慎重に積み上げていく観測者。",
        "侵入警戒型": "危険を見逃さないことを最優先する防衛的判断者。",
        "均衡解析型": "感情に流されず、数値と傾向を重視する解析者。",
        "安全優先型": "最悪を想定し続けることで秩序を保つタイプ。",
        "混沌観測型": "揺らぎと直感で世界を読み取る不定形観測者。",
    }


# 判定タイプと最終ログ文言
    if total > 0:
        accuracy = correct / total * 100
    else:
        accuracy = 0

    if accuracy >= 90:
        player_type = "慎重観測型"
        final_text = "解析終了。\n一致率は高水準。記録完了。\nあなたは観測対象として記録されました。"
    elif accuracy >= 70:
        player_type = "均衡解析型"
        final_text = "解析終了。\n判断に偏りを確認。再検証が必要です。\nあなたは観測対象として記録されました。"
    elif accuracy >= 50:
        player_type = "侵入警戒型"
        final_text = "解析終了。\n判断は不安定。\n記録が続行されます。\nあなたは観測対象として記録されました。"
    else:
        player_type = "混沌観測型"
        final_text = "解析終了。\n判断基準から大きく剥離。\n観測は続行されます。\nあなたは監視対象です。"

    context = {
        "total": total,
        "correct": correct,
        "one_step_diff": one_step_diff,
        "major_diff": major_diff,
        "deviation_rate": deviation_rate,
        "level_stats_list": level_stats_list,
        "player_type": player_type,
        "type_descriptions": type_descriptions,
        "final_text": final_text,
        "type_description": type_descriptions.get(player_type, ""),
    }

    return render(request, "records/analysis.html", context)
