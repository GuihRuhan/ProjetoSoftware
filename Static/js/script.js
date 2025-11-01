const track = document.querySelector(".carousel-track");
const slides = Array.from(track.children);
let index = 0;

document.getElementById("next").addEventListener("click", () => {
    index = (index + 1) % slides.length;
    track.style.transform = `translateX(-${index * 100}%)`;
});

document.getElementById("prev").addEventListener("click", () => {
    index = (index - 1 + slides.length) % slides.length;
    track.style.transform = `translateX(-${index * 100}%)`;
});

// Auto-play a cada 5 segundos
setInterval(() => {
    index = (index + 1) % slides.length;
    track.style.transform = `translateX(-${index * 100}%)`;
}, 5000);
