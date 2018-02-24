var canvas;
var context;
var canvasWidth = 490;
var canvasHeight = 220;
var padding = 25;

var clickX_simple = [];
var clickY_simple = [];
var clickDrag_simple = [];
var paint_simple;
var canvas_simple;
var context_simple;
var offsetLeft;
var offsetTop;
/**
* Creates a canvas element.
*/

$(document).ready(function() {
    	 prepareSimpleCanvas();
	offsetLeft = document.getElementById('leftOffset').offsetWidth+15;
    offsetTop = document.getElementById('topOffset').offsetHeight+10;
});

function prepareSimpleCanvas()
{
	// Create the canvas (Neccessary for IE because it doesn't know what a canvas element is)
	var canvasDiv = document.getElementById('canvasSimpleDiv');
	canvas_simple = document.createElement('canvas');
	canvas_simple.setAttribute('width', 'inherit');
	canvas_simple.setAttribute('height', '300px');
	canvas_simple.setAttribute('id', 'canvasSimple');
	canvasDiv.appendChild(canvas_simple);
	if(typeof G_vmlCanvasManager != 'undefined') {
		canvas_simple = G_vmlCanvasManager.initElement(canvas_simple);
	}
	context_simple = canvas_simple.getContext("2d");

	// Add mouse events
	// ----------------
	$('#canvasSimple').mousedown(function(e)
	{
		// Mouse down location
		var mouseX = e.pageX - offsetLeft;
		var mouseY = e.pageY - offsetTop;

		paint_simple = true;
		addClickSimple(mouseX, mouseY, false);
		redrawSimple();
	});

	$('#canvasSimple').mousemove(function(e){
		if(paint_simple){
			addClickSimple(e.pageX - offsetLeft, e.pageY - offsetTop, true);
			redrawSimple();
		}
	});

	$('#canvasSimple').mouseup(function(e){
		paint_simple = false;
	  	redrawSimple();
	});

	$('#canvasSimple').mouseleave(function(e){
		paint_simple = false;
	});

	$('#clearCanvasSimple').mousedown(function(e)
	{
		clickX_simple = new Array();
		clickY_simple = new Array();
		clickDrag_simple = new Array();
		clearCanvas_simple();
	});

	// Add touch event listeners to canvas element
	canvas_simple.addEventListener("touchstart", function(e)
	{
		// Mouse down location
		var mouseX = (e.changedTouches ? e.changedTouches[0].pageX : e.pageX) - offsetLeft,
			mouseY = (e.changedTouches ? e.changedTouches[0].pageY : e.pageY) - offsetTop;

		paint_simple = true;
		addClickSimple(mouseX, mouseY, false);
		redrawSimple();
	}, false);
	canvas_simple.addEventListener("touchmove", function(e){

		var mouseX = (e.changedTouches ? e.changedTouches[0].pageX : e.pageX) - offsetLeft,
			mouseY = (e.changedTouches ? e.changedTouches[0].pageY : e.pageY) - offsetTop;

		if(paint_simple){
			addClickSimple(mouseX, mouseY, true);
			redrawSimple();
		}
		e.preventDefault()
	}, false);
	canvas_simple.addEventListener("touchend", function(e){
		paint_simple = false;
	  	redrawSimple();
	}, false);
	canvas_simple.addEventListener("touchcancel", function(e){
		paint_simple = false;
	}, false);
}

function addClickSimple(x, y, dragging)
{
	clickX_simple.push(x);
	clickY_simple.push(y);
	clickDrag_simple.push(dragging);
}

function clearCanvas_simple()
{
	context_simple.clearRect(0, 0, canvasWidth, canvasHeight);
}

function redrawSimple()
{
	clearCanvas_simple();

	var radius = 5;
	context_simple.strokeStyle = "#16a028";
	context_simple.lineJoin = "round";
	context_simple.lineWidth = radius;



	for(var i=0; i < clickX_simple.length; i++)
	{
		context_simple.beginPath();
		if(clickDrag_simple[i] && i){
			context_simple.moveTo(clickX_simple[i-1], clickY_simple[i-1]);
		}else{
			context_simple.moveTo(clickX_simple[i]-1, clickY_simple[i]);
		}
		context_simple.lineTo(clickX_simple[i], clickY_simple[i]);
		context_simple.closePath();
		context_simple.stroke();
	}
}
