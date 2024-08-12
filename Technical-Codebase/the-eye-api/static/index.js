function hamButtonToggle(el) {
  el.classList.toggle("change");
  if (el.classList.contains("change")) {
    document.body.style.backgroundColor = "white";
    document.body.style.overflow = "hidden";
  } else {
    document.body.style.backgroundColor = "black";
    document.body.style.overflowY = "visible";
  }
}
const hamburger = document.querySelector(".ham-container");
const nav_links = document.querySelector(".ham-nav-links");
const links = document.querySelectorAll(".ham-nav-links li");
hamburger.addEventListener("click", () => {
  nav_links.classList.toggle("open");
  links.forEach((link) => {
    link.classList.toggle("fade");
  });
});
