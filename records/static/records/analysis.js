document.addEventListener("DOMContentLoaded", () => {
    const dataEl = document.getElementById("stats-data");
    if (!dataEl) return;

    const total = Number(dataEl.dataset.total);
    const correct = Number(dataEl.dataset.correct);
    const oneStepDiff = Number(dataEl.dataset.oneStep);
    const majorDiff = Number(dataEl.dataset.major);
    const deviation = Number(dataEl.dataset.deviation);

    function animateCount(id, end) {
        const el = document.getElementById(id);
        if (!el) return;
        let current = 0;
        const step = Math.max(1, Math.floor(end / 60));
        const interval = setInterval(() => {
            current += step;
            if (current >= end) {
                el.textContent = end;
                clearInterval(interval);
            } else {
                el.textContent = current;
            }
        }, 16);
    }

    animateCount("total", total);
    animateCount("correct", correct);
    animateCount("one_step_diff", oneStepDiff);
    animateCount("major_diff", majorDiff);
    animateCount("deviation_rate", deviation);
});
