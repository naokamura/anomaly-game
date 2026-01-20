def get_player_type(judgements):
    total = judgements.count()
    if total == 0:
        return None

    correct = 0
    low_bias = 0
    high_bias = 0

    for j in judgements:
        if j.judgement == j.record.anomaly_level:
            correct += 1
        elif j.judgement < j.record.anomaly_level:
            low_bias += 1
        else:
            high_bias += 1

    accuracy = correct / total

    if accuracy >= 0.8 and low_bias > high_bias:
        return "慎重観測型"
    if accuracy >= 0.7 and high_bias > low_bias:
        return "侵入警戒型"
    if abs(low_bias - high_bias) <= total * 0.2:
        return "均衡解析型"
    if accuracy < 0.5 and low_bias > high_bias:
        return "安全優先型"

    return "混沌観測型"
