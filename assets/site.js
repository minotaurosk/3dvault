// Ekran görüntüsüne tıklayınca büyük göster
(function () {
  var lb = document.getElementById("lb");
  if (!lb) return;
  var img = lb.querySelector("img");
  document.querySelectorAll(".shot img").forEach(function (el) {
    el.addEventListener("click", function () {
      img.src = el.currentSrc || el.src;
      img.alt = el.alt;
      lb.classList.add("on");
    });
  });
  lb.addEventListener("click", function () { lb.classList.remove("on"); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") lb.classList.remove("on"); });
})();
