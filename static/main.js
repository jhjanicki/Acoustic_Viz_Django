
// global variables


// data being mapped

var mappedData = {
			dataDisplayed: data,
			datasetDisplayed: data,
			radial_labels: [],
			segment_labels: ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
			numSegments: mappedData.segment_labels.length,
			index_one: 0 ,
			dateStart: {key:'2016-10-29'},
			dateEnd: {key:'2017-02-15'},
			siteID: {key:'GESASHIOP'},
			currentRange: options.range_blue
		}





// loaded initially

getRadialLabels(dataDisplayed);
drawSlider(dataDisplayed);


var cleanData = (function(mappedData) {
	var external = {};
	return external;
})(mappedData);

var drawData = (function() {
	var external = {};
	return external;
})();

var getData = (function(){
	var external = {};
	return external;
})();

var updateData = (function() {
	var external = {};
	return external;
})();

var options = (function() {
	var external = {};
	external.range_blue = ["#ffffd9", "#7fcdbb", "#225ea8"];
	external.range_red = ['#fef0d9','#fc8d59','#b30000'];
	external.range_pink= ['#feebe2','#f768a1','#7a0177'];
	return external;
})();



/* populate select options */
$.getJSON('/get-sites/')		
		// when the data comes back from the server
		.done(function(data) {	
			console.log(data);
			var sitesArray = data;
			$.each(sitesArray,function(index, value) 
				{ /* console.log(value); */
				    $("#site-select").append('<option value=' + value.siteID + '>' + value.siteName + '</option>');
				});
		});
		
//draw first chart


var chart = d3.acoustic.circularHeat()
	.domain([0,0.5, 1])// should make this dynamic
	.range(currentRange)
	.radialLabels(radial_labels)
	.segmentLabels(segment_labels)
	._index(index_one);
	
chart.accessor(function (d) {
	return d.Average;
})

d3.select("#chart")
	 .datum(dataDisplayed)
	 .call(chart);

//hover effect params
var innerRadius = chart.innerRadius();
var numSegments = chart.numSegments();
var segmentHeight = chart.segmentHeight();
var offset = chart.offset();
var svg = d3.select("#chart");

// call mouseover event
chart.on("customHover", mouseover(svg,index_one,innerRadius,numSegments,segmentHeight,dataDisplayed));
