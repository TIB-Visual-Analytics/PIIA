$(document).ready(function() {


    function zoomed() {
        that_svg.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
    }



    var width = $("#ex1").width();
    var height = $("#ex1").height();

    var zoom = d3.behavior.zoom()
        .scaleExtent([1, 10])
        .on("zoom", zoomed);

    var that_svg = d3.select("#ex1").append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("fill", "white")
        .attr("transform", "translate(" + 10 + "," + 10 + ")");

    var svg = that_svg.append("g")

    var force = d3.layout.force()
        .gravity(.05)
        .distance(300)
        .charge(-100)
        .size([width, height]);

    
    function reset_name_list(){
        var json_file = "graphFile.0.833.json";
        var path = "results/"+$('input[name=domain]:checked').val()+"/";
        var keep = [];
        $("input:checkbox:checked").each(function(index){
            keep.push(this.value);
        });

        d3.json((path+json_file), function(_json){
            var json = jQuery.extend(true, {}, _json);
            var n_sorted = json.nodes.sort(function(a, b) {
                if(a.name < b.name) return -1;
                if(a.name > b.name) return 1;
                return 0;
            });
            $("#button_div").empty();
            n_sorted.forEach(element => {
                var name = element.name;
                if (keep.indexOf(name) != -1){
                    var r = $('<input type="checkbox" value="'+name+'" checked>'+name+'</input></br>');
                }else{
                    var r = $('<input type="checkbox" value="'+name+'">'+name+'</input></br>');
                }
                r.click(function() {
                    filter(_json);
                });
                $("#button_div").append(r);
            });
            filter(_json);
        });
    }

    reset_name_list();

    $('input[name=domain]').click(function(){
        reset_name_list();
    });

    function filter(_json){
        var json = jQuery.extend(true, {}, _json);
        var json_file = "graphFile.0.833.json";
        var path = "results/"+$('input[name=domain]:checked').val()+"/";

        var jsonEdit = {
            "nodes": [],
            "links": []
        };
        var remove_names = [];
        var remove_positions = [];

        $("input:checkbox:not(:checked)").each(function(index){
            remove_names.push(this.value);
        });

        json.nodes.forEach(function (n, i) {
            if(remove_names.indexOf(n.name) != -1){
                remove_positions.push(i);
            }else{
                jsonEdit.nodes.push(n);
            }
        });

        json.links.forEach(function (l, i) {
            var s_nr = l.source;
            var t_nr = l.target;
            var s_name = json.nodes[s_nr].name;
            var t_name = json.nodes[t_nr].name;
            if(remove_positions.includes(s_nr) || remove_positions.includes(t_nr)){
            }else{
                jsonEdit.nodes.forEach(function (n, i) {
                    if(s_name == n.name){
                        l.source = i;
                    }else if(t_name == n.name){
                        l.target = i;
                    }
                });
                jsonEdit.links.push(l);
            }
        });
        
        createCompleteGraph(jsonEdit);
    }

    function createCompleteGraph(json){
        $("g").remove();
        var svg = that_svg.append("g")

        force
          .nodes(json.nodes)
          .links(json.links)
          .start();

        var link = svg.selectAll(".link")
            .data(json.links)
            .enter().append("line")
            .attr("class", "link")
            .style("stroke-width", function(d) { return Math.sqrt(d.weight) })
            .style("stroke", "#aaa");

        var node = svg.selectAll(".node")
            .data(json.nodes)
            .enter().append("g")
            .attr("class", "node")
            .call(force.drag);

        node.append("circle")
            .style("fill", function(d) { return randomColor({luminosity: 'light', seed: d.name}); })
            .attr("r", function(d) {
            return Math.sqrt(d.count)});

        node.append("text")
            .attr("dx", 12)
            .attr("dy", ".35em")
            .text(function(d) { return d.name })
            .style("font-family", "Helvetica, sans-serif")
            .style("fill", "#000000")
            .style("font-size", 180);

        force.on("tick", function() {
            link.attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });

            node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
        });
    }

});

