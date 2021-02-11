function ajaxGetRequest(path, callback) {
  let request = new XMLHttpRequest();
  request.onreadystatechange = function() {
    if (this.readyState===4 && this.status ===200) {
      callback(this.response);
    }
  }
  request.open("GET", path);
  request.send();
}
function showGraph (response){
  let resp = JSON.parse(response);
  var data = [
              {
                x: resp.x,
                y: resp.y,
                type: 'bar'
              }
            ];
  Plotly.newPlot("myDiv" ,data);
}
function getData(){
  ajaxGetRequest("/permitsByMonth",showGraph)
  ajaxGetRequest("/permitsByYear", showGraph)
  ajaxGetRequest("/permitsScatter", showGraph)
}


