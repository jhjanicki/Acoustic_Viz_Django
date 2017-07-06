//default values
var siteID = {key:'GESASHIOP'};
var dateStart = {key:'2016-10-29'};
var dateEnd = {key:'2017-01-15'};


// 1. user selects site


$("#site-select").on('change',function(){
	var selectedSite = $( "#site-select" ).val();
	siteID.key=selectedSite;
	
	$("#selectedsite").text = $( "#site-select option:selected" ).text();
	
	$.getJSON('/get-data/', 
			{date_start: dateStart.key, date_end:dateEnd.key, site_id: siteID.key })		
		// when the data comes back from the server
		.done(function(data) {	
			console.log(data);
			var dataCleanedArray = [];
			data.forEach(function(d){
				var dataCleaned = {};
				dataCleaned['Day']=d.date_recorded;
				dataCleaned['Time']=d.time_recorded;
				dataCleaned['Average']=d.average;
				dataCleanedArray.push(dataCleaned);
			})
			console.log(dataCleanedArray);
			/*
for (var i = 0; i < dataCleanedArray.length; i++)
				{
				   if (i % 2 !== 0)
				   {
				     dataCleanedArray.splice(i, 1);
				   }
				}
*/
			
			
			console.log(dataCleanedArray.length);
			
			dataCleanedArray.forEach(function(d,i){
				//console.log(d);
				var middle = d.Time.slice(-5);

				/* middle = middle.slice(0,2); */
				//console.log(middle);
				if(d.Time.slice(-5)!='00:00'){
					console.log(true);
					dataCleanedArray.splice(i,1);
				}
				/*
var end = d.Time.slice(-1,2);
				console.log(end);
				if(end!='00'){
					dataCleanedArray.splice(i,1);
				}
*/
				

			});
			
			console.log(dataCleanedArray.length);
			console.log(dataCleanedArray);

			dataDisplayed = dataCleanedArray;
			datasetDisplayed = dataCleanedArray;
			radial_labels = []; 
			getRadialLabels(dataDisplayed);
			swapDataset(dataDisplayed,radial_labels);
			console.log(radial_labels);
			segmentHeight = (500 - 2 * innerRadius) / (2 * radial_labels.length);
			// should make this dynamic
    		offset = innerRadius + Math.ceil(dataDisplayed.length / numSegments) * segmentHeight;
    		index=0;
    		chart.on("customHover", mouseover(svg,index,innerRadius,numSegments,segmentHeight,dataDisplayed));
		});
	
	
});





// 2. slider populated with earliest start date in data and latest end date






/* populate select options */
$.getJSON('/get-sites/')		
		// when the data comes back from the server
		.done(function(data) {	
			console.log(data);
			var sitesArray = data;
			$.each(sitesArray,function(index, value) 
				{
					console.log(value);
				    $("#site-select").append('<option value=' + value.siteID + '>' + value.siteName + '</option>');
				});
		});