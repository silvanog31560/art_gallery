// product_list.html sorting

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
const drop_btn = document.querySelector(".dropbtn");
const review_btn = document.querySelector(".review-btn-menu");

if (drop_btn){
  drop_btn.addEventListener("click", myFunction);
}

if (review_btn){
  review_btn.addEventListener("click", reviewFunction);
}

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


// review_list.html

function reviewFunction(){
  var x = document.getElementById("review-menu");
  x.classList.toggle('hide');
}
