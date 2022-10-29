// product_list.html sorting

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
const drop_btn = document.querySelector(".dropbtn");
const review_btn = document.querySelector(".review-btn-menu");

function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

drop_btn.addEventListener("click", myFunction);

// review_list.html
// const is at top

function reviewFunction(){
  var x = document.getElementById("review-menu");
  x.classList.toggle('hide');
}

review_btn.addEventListener("click", reviewFunction);
