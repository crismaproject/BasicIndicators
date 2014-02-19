/*
 Peter.Kutschera@ait.ac.at, 2014-02-11
 Time-stamp: "2014-02-19 08:52:57 peter"

    Copyright (C) 2014  AIT / Austrian Institute of Technology
    http://www.ait.ac.at
 
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 2 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
 
    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see http://www.gnu.org/licenses/gpl-2.0.html
*/

function drawIndicators ( containerName, allIndicators, byWorldstate ) {

    // console.log ("allIndicators = " + JSON.stringify (allIndicators));
    // console.log ("byWorldstate = " + byWorldstate);

    var worldstates = d3.keys (allIndicators); // ["81", "82"];
    // console.log ("worldstates: " + worldstates);
    var indicators = [] //["deathsIndicator", "seriouslyDeterioratedIndicator", "improvedIndicator"];
    for (var k = 0; k < worldstates.length; k++) {
	allIndicators[worldstates[k]].forEach (function (d) {
	    if ((d.type === "number") || (d.type === "histogram")) {
		if (indicators.indexOf (d.id) == -1) {
		    indicators.push (d.id);
		}
	    }
	});
    };
    // console.log ("indicators: " + indicators);

    if (byWorldstate) {
	var groups = worldstates;
	var bars = indicators;
	var data = []; // [{group: "81", bars: [{id: "deathsIndicator", value: 1}, {id: "seriouslyDeterioratedIndicator", value: 10}, {id: "improvedIndicator", value: 39}]}, ...]
	for (var k = 0; k < worldstates.length; k++) {
	    var b = [];
	    allIndicators[worldstates[k]].forEach (function (d) {
		if (indicators.indexOf (d.id) >= 0) {
		    if (d.type === "number") {
			b.push ({id: d.id, values: [{id: d.id, name: 'value', y0: 0, y1: d.data}], max: d.data});
		    } else if (d.type === "histogram") {
			var y0 = 0;
			var vs = [];
			for (var i = 0; i < d.data.length; i++) {
			    vs.push ({id: d.id, name: d.data[i].key, y0: y0, y1: y0 +=  d.data[i].value, color: d.data[i].color});
			}
			b.push ({id: d.id, values: vs, max: y0});
		    }		    
		}
	    });
	    data.push ({group: worldstates[k], bars: b});
	}
	// console.log ("data: " + JSON.stringify (data));
	drawIndicatorBars (containerName, groups, bars, data);
    } else {
	var groups = indicators;
	var bars = worldstates;
	var data = []; // [{group: "deathsIndicator", bars: [{id: "81", value: 1}, ...
	for (var i = 0; i < indicators.length; i++) {
	    var b = [];
	    for (var k = 0; k < worldstates.length; k++) {
		for (var j = 0; j < allIndicators[worldstates[k]].length; j++) {
		    var d = allIndicators[worldstates[k]][j];
		    if (indicators[i] === d.id) {
			if (d.type === "number") {
			    b.push ({id: worldstates[k], values: [{id: worldstates[k], name: 'value', y0: 0, y1: d.data}], max: d.data});
			} else if (d.type === "histogram") {
			    var y0 = 0;
			    var vs = [];
			    for (var l = 0; l < d.data.length; l++) {
				vs.push ({id: worldstates[k], name: d.data[l].key, y0: y0, y1: y0 +=  d.data[l].value, color: d.data[l].color});
			    }
			    b.push ({id: d.worldstates[k], values: vs, max: y0});
			}
		    }
		};
	    }
	    data.push ({group: indicators[i], bars: b});
	}
	// console.log ("data: " + JSON.stringify (data));
	drawIndicatorBars (containerName, groups, bars, data);
    }

}

function drawIndicatorBars ( containerName, groups, bars, data ) {
    /*
    console.log ("groups: " + JSON.stringify (groups));
    console.log ("bars:   " + JSON.stringify (bars));
    console.log ("data:   " + JSON.stringify (data));
    */

    groups = groups.sort();
    bars = bars.sort();

    $(containerName).empty();

    var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 300 - margin.top - margin.bottom;

    var x0 = d3.scale.ordinal()
	.rangeRoundBands([0, width], .1);

    var x1 = d3.scale.ordinal();

    var y = d3.scale.linear()
	.range([height, 0]);

    var color = d3.scale.ordinal()
	.range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

    var xAxis = d3.svg.axis()
	.scale(x0)
	.orient("bottom");

    var yAxis = d3.svg.axis()
	.scale(y)
	.orient("left")
	.tickFormat(d3.format(".2s"));

    var svg = d3.select(containerName).append("svg")
	.attr("width", width + margin.left + margin.right)
	.attr("height", height + margin.top + margin.bottom)
	.append("g")
	.attr("class", "container")
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");


    color.domain (bars);
    x0.domain(groups);
    x1.domain(bars).rangeRoundBands([0, x0.rangeBand()]);
    y.domain([0, d3.max(data, function(d) { return d3.max(d.bars, function(d) { return d.max; }); })]);

    svg.append("g")
	.attr("class", "x axis")
	.attr("transform", "translate(0," + height + ")")
	.call(xAxis);

    svg.append("g")
	.attr("class", "y axis")
	.call(yAxis)
	.append("text")
	.attr("transform", "rotate(-90)")
	.attr("y", 6)
	.attr("dy", ".71em")
	.style("text-anchor", "end")
	.text("Indicator-Value");

    var state = svg.selectAll(".group")
	.data(data)
	.enter().append("g")
	.attr("class", "g")
	.attr("transform", function(d) { return "translate(" + x0(d.group) + ",0)"; });

    var subbars = state.selectAll("rect")
	.data(function(d) { var a = []; d.bars.forEach (function (b) {a = a.concat (b.values);}); return a; })
        .enter().append("rect")
	.attr("width", x1.rangeBand())
	.attr("x", function(d) { return x1(d.id); })
	.attr("y", function(d) { return y(d.y1); })
	.attr("height", function(d) { return y(d.y0) - y(d.y1) + 1; })
	.style("fill", function(d) { return d.color ? d.color : color(d.id); })
	.style("stroke-width", 2)
	.style("stroke", function(d) { return color(d.id); });

    var legend = svg.selectAll(".legend")
	.data(bars.slice().reverse())
	.enter().append("g")
	.attr("class", "legend")
	.attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

    legend.append("rect")
	.attr("x", width - 18)
	.attr("width", 18)
	.attr("height", 18)
	.style("fill", color);

    legend.append("text")
	.attr("x", width - 24)
	.attr("y", 9)
	.attr("dy", ".35em")
	.style("text-anchor", "end")
	.text(function(d) { return d; });


};


