document.addEventListener("DOMContentLoaded", () => {
    const titles = document.querySelectorAll(".glitch-title");

    titles.forEach(title => {
        setInterval(() => {
            title.classList.toggle("glitch");
        }, 1500);
    });
});
