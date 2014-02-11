/*
 Peter.Kutschera@ait.ac.at, 2013-10-17
 Time-stamp: "2014-02-11 16:57:11 peter"

 See http://blog.pixelingene.com/2011/07/building-a-tree-diagram-in-d3-js/

*/
/*

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
  
var selectedWS = [];
var selectWSfunc = null;

function createWorldStateTree(containerName, wsid, list, selectWSfunction, renderOptions) {
    selectWSfunc = selectWSfunction;
    $(containerName).empty();
    // create tree from WS list
    var treeData = getFromList (wsid, list);
    // console.log (JSON.stringify (treeData));
	
    // build the options object
    var options = $.extend({
        nodeRadius: 5, fontSize: 12
    }, renderOptions);
    
    // Calculate total nodes, max label length
    var totalNodes = 0;
    var maxLabelLength = 0;
    visit(treeData, 
	  function(d) {
	      totalNodes++;
	      maxLabelLength = Math.max(d.label.length, maxLabelLength);
	  }, 
	  function(d) {
	      return d.children && d.children.length > 0 ? d.children : null;
	  });

    // size of the diagram
    var size = { width:$(containerName).outerWidth(), height: totalNodes * 15};

    var tree = d3.layout.tree()
        .sort(null)
        .size([size.height, size.width - maxLabelLength*options.fontSize])
        .children(function(d) {
	    return (!d.children || d.children.length === 0) ? null : d.children;
        });

    var nodes = tree.nodes(treeData);
    var links = tree.links(nodes);

    
    /*
      <svg>
      <g class="container" />
      </svg>
    */
    var layoutRoot = d3.select(containerName)
        .append("svg:svg").attr("width", size.width).attr("height", size.height)
        .append("svg:g")
        .attr("class", "container")
        .attr("transform", "translate(" + maxLabelLength + ",0)");


    // Edges between nodes as a <path class="link" />
    var link = d3.svg.diagonal()
        .projection(function(d)
		    {
			return [d.y, d.x];
		    });

    layoutRoot.selectAll("path.link")
        .data(links)
        .enter()
        .append("svg:path")
        .attr("class", "link")
        .attr("d", link);


    /*
      Nodes as
      <g class="node">
      <circle class="node-dot" />
      <text />
      </g>
    */
    var nodeGroup = layoutRoot.selectAll("g.node")
        .data(nodes)
        .enter()
        .append("svg:g")
        .attr("class", "node")
        .attr("transform", function(d)
	      {
		  return "translate(" + d.y + "," + d.x + ")";
	      });

    nodeGroup.append("svg:circle")
        .attr("class", "node-dot")
        .attr("r", options.nodeRadius)
        // .on ("click", function (d) {alert (d.wsid)});
	// .on ("click", function (d) {alert (JSON.stringify (d.data))});
	.on ("click", function (d) {
	    // console.log ("shiftKey: " + d3.event.shiftKey);
	    // console.log ("ctrlKey:  " + d3.event.ctrlKey);
	    // d3.selectAll(".node-selected").attr("class", "node-dot");
	    // d3.select(this).attr("class", "node-selected");
	    // selectWSfunction (d.wsid);
	    selectNode (d.wsid, d3.event.shiftKey, d3.event.ctrlKey);
	});

    nodeGroup.append("svg:text")
        .attr("text-anchor", function(d)
	      {
		  return d.children ? "end" : "start";
	      })
        .attr("dx", function(d)
	      {
		  var gap = 2 * options.nodeRadius;
		  return d.children ? -gap : gap;
	      })
        .attr("dy", -7)
        .text(function(d)
	      {
		  return d.label;
	      });

    nodeGroup.append("svg:text")
        .attr("text-anchor", "middle")
        .attr("dx", 0)
        .attr("dy", 7 + options.fontSize)
        .text(function(d)
	      {
		  return d.data.dateTime.substring (11, 16);
	      });
}

/*
  childrenFn: function fo find children nodes of parent node
  visitFn: function applied to each node
*/
function visit(parent, visitFn, childrenFn) {
    if (!parent) return;
    visitFn(parent);
    var children = childrenFn(parent);
    if (children) {
        var count = children.length;
        for (var i = 0; i < count; i++) {
            visit(children[i], visitFn, childrenFn);
        }
    }
}



function selectNode (wsid, shiftKey, ctrlKey) {
    if (!(shiftKey || ctrlKey)) {
	// take this one
	selectedWS = [wsid];
    } else if (ctrlKey && !shiftKey) {
	// add or remove
	var i = selectedWS.indexOf (wsid);
	if (i == -1) {
	    selectedWS.push (wsid);
	} else {
	    selectedWS.splice (i, 1);
	}
    } else if (shiftKey && !ctrlKey) {
	// Add all between this and what?
    }
    d3.selectAll(".node-dot, .node-selected").attr("class", function (d) {
	if (selectedWS.indexOf (d.wsid) == -1) {
	    return "node-dot";
	} else {
	    return "node-selected";
	}
    });
    selectWSfunc (selectedWS);
}
	    


////////////////////////
/*
  get tree of WorldStates from list of all WorldStates
  Start with wsid
*/
function getFromList (wsid, list) {
    // console.log ("getFromList (" + wsid + ", list)");
    var tmp = { wsid : wsid, label: "id: " + wsid, children : [] };
    for (var i = 0; i < list.length; i++) {
	if (list[i]["worldStateId"] === wsid) {
	    tmp.data = list[i];
	    if (list[i].description) {
		tmp.label = list[i].description;
	    }
	    // Neither <br> nor \n works :-(
	    //	    if (list[i].dateTime) {
	    //		tmp.label += "\n" + list[i].dateTime;
	    //	    }
	    break;
	}
    }
    //    console.log ("label = " + tmp.label);
    for (var i = 0; i < list.length; i++) {
	if (list[i]["worldStateParentId"] === wsid) {
	    tmp['children'].push (getFromList (list[i]["worldStateId"], list));
	}
    }
    return tmp;
}

