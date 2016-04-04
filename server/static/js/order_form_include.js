var counter = 1;
var limit = 3;
function addInput(divName){
     if (counter == limit)  {
          alert("You have reached the limit of adding " + counter + " inputs");
     }
     else {
          var newdiv = document.createElement('div');
          newdiv.innerHTML = "Seat " + (counter + 1) + " OMGWOWAAAAAAA";
          document.getElementById(divName).appendChild(newdiv);
          counter++;
     }
}
