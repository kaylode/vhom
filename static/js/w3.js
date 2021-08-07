function onClick(e) {
  console.log(this.getLatLng());
}

function w3_open() {
    document.getElementById("main").style.marginLeft = "25%";
    document.getElementById("mySidebar").style.width = "25%";
    document.getElementById("mySidebar").style.display = "block";
    document.getElementById("openNav").style.display = 'none';
  }
  
function w3_close() {
document.getElementById("main").style.marginLeft = "0%";
document.getElementById("mySidebar").style.display = "none";
document.getElementById("openNav").style.display = "inline-block";
}