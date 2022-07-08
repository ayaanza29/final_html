//if (job.current_step != 3){
const fileInput = document.querySelector("#upload");
// <link rel= "stylesheet" type= "text/css" href= "{{ url_for('static',filename='css/style.css') }}"></link>
// src= "https://code.jquery.com/jquery-3.6.0.min.js"
// enabling drawing on the blank canvas
drawOnImage();

// fileInput.addEventListener("change", async (e) => {
//   const [file] = fileInput.files;
  
//   // displaying the uploaded image
//   const image = document.createElement("img");
//   image.src = await fileToDataUri(file);
  
//   // enabling the brush after the image
//   // has been uploaded
//   image.addEventListener("load", () => {
//     drawOnImage(image);
//   });
  
//   return false;
// });

// jQuery.ajax({type: "GET", 
//   url:"/new",
//   data: {"path": "C:/Users/Zuhayr/Documents/GitHub/r_background_app/PeacoQC_results/fcs_files/776 F SP_QC.fcs"},
// }).done(function(data){
//   alert("done");
//   const image = document.createElement("img");
//   image.src = "static/temporary_images/plot3.png";
//   image.addEventListener("load", () => {
//     drawOnImage(image);
//   });
// }); 

var path_cleaned_fcs_files = job.path + "qc_cleaned_fcs/PeacoQC_results/fcs_files/776_F_SP_QC_QC.fcs" //"C:/Users/Zuhayr/Documents/GitHub/r_background_app/PeacoQC_results/fcs_files/776 F SP_QC.fcs" "F:\user_data\tom\wow\qc_cleaned_fcs\PeacoQC_results\fcs_files\776 F SP_QC_QC.fcs"
var path_images = job.path + "gating/temporary_images/mark1.png"
console.log("path for graphing " + path_cleaned_fcs_files)

jQuery.ajax({type: "GET", 
      url:"/new",
      data: {"path": path_cleaned_fcs_files, "list_points": "all"},
    }).done(function(){
      alert("done");
      // const image = document.createElement("img");
      // image.src = "static/temporary_images/mark1.png";
      // image.addEventListener("load", () => {
      //   drawOnImage(image);
      // });
      // const imageWidth = image.width;
      // const imageHeight = image.height;
      // canvasElement.width = imageWidth;
      // canvasElement.height = imageHeight;
      // context.drawImage(image, 0, 0, imageWidth, imageHeight);
      // jQuery.ajax({type: "GET", 
      //   url:"/rerender",
      // })
      const image = document.createElement("img");
      image.src = "static/temporary_images/mark1.png";

      image.addEventListener("load", () => {
        drawOnImage(image);
      });

    });

function updateAxis() {
  jQuery.ajax({type: "GET", 
    url:"/new",
    data: {"path": path_cleaned_fcs_files, "list_points": "all", "x_axis": x_axis, "y_axis": y_axis},
  }).done(function(){
    alert("done");
    // const image = document.createElement("img");
    // image.src = "static/temporary_images/mark1.png";

    const image = document.createElement("img");
    image.src = "static/temporary_images/mark1.png?rnd="+Math.random();
    // document.getElementById("img").src = "static/temporary_images/mark1.png";

    image.addEventListener("load", () => {
      drawOnImage(image);
    });
    // jQuery.ajax({type: "GET", 
    //   url:"/rerender",
    //   //data: {"path": "C:/Users/Zuhayr/Documents/GitHub/r_background_app/PeacoQC_results/fcs_files/776 F SP_QC.fcs", "list_points": "all", "x_axis": x_axis, "y_axis": y_axis},
    // })
  });
}

// const choose_x_axis = document.getElementsByName("x-axis");
// let x_axis = "";
// choose_x_axis.forEach((x) => {
//   if (x.checked) x_axis = x.value;
// });
// choose_x_axis.forEach((x) => {
//   x.onclick = () => {
//     x_axis = x.value;
//     console.log("x_change")
//     updateAxis()
//   };
// });

// const choose_y_axis = document.getElementsByName("y-axis");
// let y_axis = "";
// choose_y_axis.forEach((y) => {
//   if (y.checked) y_axis = y.value;
// });
// choose_y_axis.forEach((y) => {
//   y.onclick = () => {
//     y_axis = y.value;
//     console.log("y_change")
//     updateAxis()
//   };
// });

var x_select = document.getElementById('x_axis');
x_select.onchange = function() {
  let x_axis = "";
  var x_text = (x_select.options[x_select.selectedIndex]).text;
  x_axis = x_text
  console.log("x change ");
  console.log(x_text);
  updateAxis()
}

var y_select = document.getElementById('y_axis');
y_select.onchange = function() {
  let y_axis = "";
  var y_text = (y_select.options[y_select.selectedIndex]).text;
  y_axis = y_text
  console.log("y change ");
  console.log(y_text);
  updateAxis()
}

// const x_btn = document.getElementById("x_button");

// x_btn.addEventListener("click", ()=>{
//   x_btn.innerText
// })



// const image = document.createElement("img");
// image.src = "static/temporary_images/mark1.png";

// image.addEventListener("load", () => {
//   drawOnImage(image);
// });



function fileToDataUri(field) {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.addEventListener("load", () => {
      resolve(reader.result);
    });
    reader.readAsDataURL(field);
  });
}

// const sizeElement = document.querySelector("#sizeRange");
// let size = sizeElement.value;
// sizeElement.oninput = (e) => {
//   size = e.target.value;
// };

// const colorElement = document.getElementsByName("colorRadio");
// let color;
// colorElement.forEach((c) => {
//   if (c.checked) color = c.value;
// });
// colorElement.forEach((c) => {
//   c.onclick = () => {
//     color = c.value;
//   };
// });
let color = "black";

const chooseShape = document.getElementsByName("chooseShape");
let shape = "";
chooseShape.forEach((s) => {
  if (s.checked) shape = s.value;
});
chooseShape.forEach((s) => {
  s.onclick = () => {
    shape = s.value;
  };
});



// const x_axis = document.getElementsByName("x-axis");
// let x_axis_name = "";

// });

function dist(x0,y0,x1,y1){
  return Math.sqrt( Math.pow(x1-x0,2) + Math.pow(y1-y0,2));
}

CanvasRenderingContext2D.prototype.fillPolygon = function (pointsArray, fillColor, strokeColor) {
  if (pointsArray.length <= 0) return;
  this.moveTo(pointsArray[0][0], pointsArray[0][1]);
  for (var i = 0; i < pointsArray.length; i++) {
      this.lineTo(pointsArray[i][0], pointsArray[i][1]);
  }
  if (strokeColor != null && strokeColor != undefined)
      this.strokeStyle = strokeColor;

  if (fillColor != null && fillColor != undefined) {
      this.fillStyle = fillColor;
      this.globalAlpha = 0.7;
      this.fill();
  }
}



function drawOnImage(image = null) {
  const canvasElement = document.getElementById("canvas");
  
  const context = canvasElement.getContext("2d");
  
  // if an image is present,
  // the image passed as parameter is drawn in the canvas
  if (image) {
    const imageWidth = image.width;
    const imageHeight = image.height;
    
    // rescaling the canvas element
    canvasElement.width = imageWidth;
    canvasElement.height = imageHeight;
    
    context.drawImage(image, 0, 0, imageWidth, imageHeight);
  }
  
  const clearElement = document.getElementById("clear");
  clearElement.onclick = () => {
    // context.clearRect(0, 0, canvasElement.width, canvasElement.height);
    if (image) {
      const imageWidth = image.width;
      const imageHeight = image.height;
      
      // rescaling the canvas element
      canvasElement.width = imageWidth;
      canvasElement.height = imageHeight;
      
      context.drawImage(image, 0, 0, imageWidth, imageHeight);
    }
  };

  const nextElement = document.getElementById("next");
  nextElement.onclick = () => {
    // context.clearRect(0, 0, canvasElement.width, canvasElement.height);
    // if (image) {
    //   const imageWidth = image.width;
    //   const imageHeight = image.height;
      
    //   // rescaling the canvas element
    //   canvasElement.width = imageWidth;
    //   canvasElement.height = imageHeight;
      
    //   context.drawImage(image, 0, 0, imageWidth, imageHeight);
    // }

    // jQuery.ajax({
    //   type: "GET",
    //   url: "/static/new_graph_still_image.py",
    //   // data: { param: text}
    //   // data: {"thing1", "thing2"};
    //   runstuff: function(stuff){"thing1", "thing2"},
    // }).done(function() {
    //   alert("calculated")
    // });

    // jQuery.get("/static/new_graph_still_image.py/cool", function(stuff) {
    //   console.log(stuff)
    // })


    // this.ncode= jQuery('next');
    // this.ncode.on('click', function () {
    // // var scode = jQuery('#prqcd').val();
    // jQuery.ajax({type: "GET",
    //   url:'/static/new_graph_still_image.py',
    //   // data: { param: "hi"}
    //   // data: {'scode ': scode , 'task': 'addcode', 'format': 'json'},
    //   // dataType: 'json',
    //   success: function (response)
    //   {
    //     console.log(response)
    //     alert("hi")
    //   }
    // });
    // });

    build_string_array = "[(";
    i = 0;
    while (i < context.shifted_list_points.length){
      build_string_array += context.shifted_list_points[i];
      build_string_array += "), ("
      i++;
    }
    build_string_array = build_string_array.substring(0, build_string_array.length - 3)
    build_string_array += "]"
    console.log(build_string_array)
    console.log(context.shifted_list_points.toString());


    
    //image.src = "static/temporary_images/mark1.png";
    // xyz = "cool"
    jQuery.ajax({type: "GET", 
      url:"/new",
      data: {"path": path_cleaned_fcs_files, "list_points": build_string_array},
      // dataType: "text",
      // success: function(response) {
      //   output = response;
      //   alert(output);
      //   const image = document.createElement("img");
      //   image.src = "static/temporary_images/plot3.png";
      //   image.addEventListener("load", () => {
      //     drawOnImage(image);
      //   });
      //   const imageWidth = image.width;
      //   const imageHeight = image.height;
      //   canvasElement.width = imageWidth;
      //   canvasElement.height = imageHeight;
      //   context.drawImage(image, 0, 0, imageWidth, imageHeight);
      // }
    }).done(function(data){
      // console.log(data);
      alert("done");
      const image = document.createElement("img");
      image.src = "static/temporary_images/mark1.png?rnd="+Math.random();
      image.addEventListener("load", () => {
        drawOnImage(image);
      });
      const imageWidth = image.width;
     const imageHeight = image.height;
     canvasElement.width = imageWidth;
     canvasElement.height = imageHeight;
     context.drawImage(image, 0, 0, imageWidth, imageHeight);
      //document.body.appendChild(image)
      canvas = document.getElementById('canvas');
      ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(image, 0, 0, imageWidth, imageHeight);
      
    });

    
  };

  context.x0 = -999999
  context.y0 = -999999
  context.list_points = [[]]
  start_flag = false
  
  this.strokeStyle = "rgba(128, 128, 128, 0.5)";
  this.fillColor = "rgba(128, 128, 128, 0.5)";
  let isDrawing;
  canvasElement.onmousedown = (e) => {
    // if (shape = null) {
    //   isDrawing = true;
    //   context.beginPath();
    //   context.lineWidth = size;
    //   context.strokeStyle = color;
    //   context.lineJoin = "round";
    //   context.lineCap = "round";
    //   context.moveTo(e.clientX, e.clientY);
    // }
    // else{
    //   isDrawing = true;
    //   context.beginPath();
    //   context.strokeStyle = color;
    //   context.initial_x = e.clientX;
    //   context.initial_y = e.clientY;
    //   context.moveTo(e.clientX, e.clientY);
    // }

    // context.shape = shape;
    // console.log(context.shape);
    // context.list_points = [[]]
    if (shape == "rectangle") {
      isDrawing = true;
      context.beginPath();
      context.strokeStyle = color;
      context.initial_x = e.clientX;
      context.initial_y = e.clientY;
      x_adjust = -158;
      y_adjust = -8;
      context.moveTo(e.clientX, e.clientY);
      // console.log("should not be ellipse1" + shape)
    }
    else if (shape == "ellipse") {
      isDrawing = true;
      // context.clearRect(0, 0, canvasElement.width, canvasElement.height);
      context.beginPath();
      context.strokeStyle = color;
      context.center_x = e.clientX;
      context.center_y = e.clientY;
      context.moveTo(e.clientX, e.clientY);
    }
    else if (shape == "polygon") {
      if (start_flag == false){
        context.list_points = [[]]
        // console.log("In start")
        isDrawing = true;
        context.beginPath();
        context.strokeStyle = color;
        context.x0 = e.clientX;
        context.y0 = e.clientY;
        x_adjust = -158;
        y_adjust = -8;
        // console.log("should be 1" + [e.clientX + x_adjust, e.clientY + y_adjust])
        context.list_points.push([e.clientX + x_adjust, e.clientY + y_adjust])
        context.moveTo(e.clientX + x_adjust, e.clientY + y_adjust);
        
        
      }
      else{
        // console.log("In continue")
        // context.lineWidth = 10;
        context.lineCap = "square";
        x_adjust = -158;
        y_adjust = -8;
        if (dist(context.x0, context.y0, e.clientX + x_adjust, e.clientY + y_adjust) < 10) {
          context.lineTo(context.x0 + x_adjust, context.y0 + y_adjust);
          context.list_points.push([context.x0 + x_adjust, context.y0 + y_adjust]);
          context.lastX = context.x0;
          context.lastY = context.y0;
        }
        else {
          context.lineTo(e.clientX + x_adjust, e.clientY + y_adjust);
          // console.log("should be 2 and 3: " + [e.clientX + x_adjust, e.clientY + y_adjust])
          context.list_points.push([e.clientX + x_adjust, e.clientY + y_adjust])
          context.lastX = e.clientX;
          context.lastY = e.clientY;
        }
        // context.line_end = 10;
        // context.fillRect(e.clientX - context.line_end, e.clientY + context.line_end, context.line_end, context.line_end);
        // console.log(e.clientX, e.clientY);
        context.stroke();
        
      }
      
    }
  };

  // myCanvas.addEventListener('dblclick', function(){ 

  //   if (shape == "rectangle"){
  //     console.log("double rect points:")
  //   }
  //   else if(shape == "ellipse"){
  //     console.log("double ellipse points:")
  //   }
  
  // });

  // canvasElement.ondblclick = (e) => {
  //   if (shape == "rectangle"){
  //     console.log("double rect points:")
  //   }
  //   else if(shape == "ellipse"){
  //     console.log("double ellipse points:")
  //   }
  // };
  
  canvasElement.onmousemove = (e) => {
    context.shape = shape;

    if (isDrawing) {    
      // console.log(shape)
      if (shape == "rectangle"){
        // context.clearRect(0, 0, canvasElement.width, canvasElement.height);
        if (image) {
          const imageWidth = image.width;
          const imageHeight = image.height;
          
          // rescaling the canvas element
          canvasElement.width = imageWidth;
          canvasElement.height = imageHeight;
          
          context.drawImage(image, 0, 0, imageWidth, imageHeight);
        }
        context.fillStyle = 'rgba(128, 128, 128, 0.5)';
        x_adjust = -158;
        y_adjust = -8;
        context.fillRect(context.initial_x + x_adjust, context.initial_y + y_adjust, e.clientX - context.initial_x + x_adjust, e.clientY - context.initial_y + y_adjust);
        
      }
      else if (shape == "ellipse"){
        // console.log("new ellipse " + shape)
        context.clearRect(0, 0, canvasElement.width, canvasElement.height);
        context.ellipse(context.center_x, context.center_y, Math.abs(e.clientX - context.center_x), Math.abs(e.clientY - context.center_y), 0, 0, 2 * Math.PI, false);
        context.stroke();
      }
      else if (shape == "polygon"){
        if (start_flag == false){
          // context.clearRect(0, 0, canvasElement.width, canvasElement.height);
          // if (image) {
          //   const imageWidth = image.width;
          //   const imageHeight = image.height;
            
          //   // rescaling the canvas element
          //   canvasElement.width = imageWidth;
          //   canvasElement.height = imageHeight;
            
          //   context.drawImage(image, 0, 0, imageWidth, imageHeight);
          // }
          start_flag = true;
        }
        
      }
    }


  };
  
  canvasElement.onmouseup = function (e) {
    if (shape == "rectangle") {
      isDrawing = false;
      context.list_points.push([context.initial_x, context.initial_y])
      context.list_points.push([e.clientX, context.initial_y])
      context.list_points.push([e.clientX, e.clientY])
      context.list_points.push([context.initial_x, e.clientY])
      context.list_points.shift();
      context.shifted_list_points = [];
      context.list_points.forEach(function(entry) {
        context.x_graph_transform = -62;
        context.y_graph_transform = -358;
        context.x_graph_multiply = 13888;
        context.y_graph_multiply = -12987;
        context.shifted_list_points.push([(entry[0] + context.x_graph_transform) * context.x_graph_multiply, (entry[1] + context.y_graph_transform) * context.y_graph_multiply]);
      });
      context.closePath();
    }
    else if (shape != "polygon") { //  || start_flag == true
      isDrawing = false;
      context.closePath();
    }
    else if (dist(context.x0, context.y0, context.lastX, context.lastY) < 20) {
      context.list_points.pop();
      context.list_points.shift();
      context.shifted_list_points = [];
      context.list_points.forEach(function(entry) {
        context.x_graph_transform = -62;
        context.y_graph_transform = -358;
        context.x_graph_multiply = 13888;
        context.y_graph_multiply = -12987;
        context.shifted_list_points.push([(entry[0] + context.x_graph_transform) * context.x_graph_multiply, (entry[1] + context.y_graph_transform) * context.y_graph_multiply]);
      });
      // context.shifted_list_points.forEach(function(entry) {
      //   console.log(entry);
      // });
      // console.log("ending path");
      context.closePath();
      // var polygonPoints = [[10,100],[20,75],[50,100],[100,100],[10,100]];
      context.fillPolygon(context.list_points, 'rgba(128, 128, 128, 0.5)','#000');
      // context.fillStyle = '#f00';
      // poly = context.list_points;
      // context.beginPath();
      // context.moveTo(poly[0], poly[1]);
      // console.log(poly[0]);
      // console.log(poly[1]);
      // for( item=2 ; item < poly.length-1 ; item+=2 ){context.lineTo( poly[item] , poly[item+1] )}
      // context.closePath();
      // context.fill();
      // context.clearRect(0, 0, canvasElement.width, canvasElement.height);
      
      isDrawing = false;
      start_flag = false;
      
      
    }
  };
}
//}