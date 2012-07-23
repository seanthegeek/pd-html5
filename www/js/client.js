/*Copyright (C) 2012 Sean Whalen

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.*/

$(document).bind('pageinit', function(event) {
	// Set the connected flag
	var connected = true;

	// Select the controls
	var start = $("#start-button");
	var pause = $("#pause-button");
	var track = $("#track-select");
	var volume = $("#volume-slider");
	var reverb = $("#reverb-slider"); 
	
    // Populate the options with a list of tracks from the server 
	$.getJSON("get_tracks", function(data) {
		$.each(data, function(index, val) {
		  track
         .append($("<option></option>")
         .attr("value", index)
         .text(val)); 
		});
	track.selectmenu("refresh");
	});
	
	function setValues() {
	$.getJSON("get_status", function(data){
		if (connected){
			if (parseInt(track.val()) != data.track){
				track.val(data.track.toString()).attr('selected', true).siblings('option').removeAttr('selected');
				track.selectmenu("refresh");
			}
			
			if (parseInt(volume.attr("value")) != data.volume){
				volume.attr("value", data.volume.toString());
				volume.slider('refresh');
			}
			
			
			if (parseInt(track.attr("value")) != data.reverb){
				reverb.attr("value", data.reverb.toString());
				reverb.slider('refresh');
			}
			
			// Update every 5 seconds
			setTimeout(function(){setValues();}, 5000)
		}
	});
}
	// Bind the events
	track.ajaxError(function() {
		connected = false;
		alert("The demonstration has ended.");
	});
	
	start.bind("click", function(event, ui) {
		$.get("play", {value: track.val()});
		});
		
	pause.bind("click", function(event, ui) {
		$.get("pause");
	});
	
	volume.bind("change", function(event, ui) {
		$.get("set_volume", {value: volume.attr("value")});
	});
	
	reverb.bind("change", function(event, ui) {
		$.get("set_reverb", {value: reverb.attr("value")});
	});
	
	// Reset the UI to reflect the current settings
	setValues();

});