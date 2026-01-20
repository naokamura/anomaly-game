document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.querySelector('.start-btn-wrap .glitch-btn');
    if(startBtn){
        startBtn.addEventListener('click', (e) => {
            e.preventDefault();
            // 遅延演出後に遷移
            startBtn.classList.add('clicked');
            setTimeout(() => {
                window.location.href = startBtn.href;
            }, 500); 
        });
    }
});
