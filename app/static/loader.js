document.addEventListener("DOMContentLoaded", function () {
  function loading() {
    document.querySelector(".loader").style.display = "block";
    document.querySelectorAll(".content").forEach(function (el) {
      el.style.display = "none";
    });
  }

  document.querySelector("form").addEventListener("submit", function () {
    loading();
  });
});
