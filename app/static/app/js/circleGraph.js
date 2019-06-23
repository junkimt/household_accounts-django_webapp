function showCircleGraph (dataset, tag_str, class_str) {

  var selector_str = tag_str + "." + class_str;


  var width = parseInt(window.innerWidth * 1.0); // グラフの幅
  //var height = parseInt(width * 0.75); // グラフの高さ
  var height = 500;

  var radius = Math.min(width, height) / 2 - 10;

  // 2. SVG領域の設定
  //var svg = d3.select("body").append("svg").attr("width", width).attr("height", height);
  var svg = d3.select(selector_str).append("svg").attr("width", width).attr("height", height);

  var translated_pos_X = parseInt(width * 0.5);
  g = svg.append("g").attr("transform", "translate(" + translated_pos_X + "," + height / 2 + ")");

  // 3. カラーの設定
  var color = d3.scaleOrdinal()
    .range(["#DC3912", "#3366CC", "#109618", "#FF9900", "#990099"]);

  // 4. pieチャートデータセット用関数の設定
  var pie = d3.pie()
    .value(function(d) { return d.value; })
    .sort(null);

  // 5. pieチャートSVG要素の設定
  var pieGroup = g.selectAll(".pie")
    .data(pie(dataset))
    .enter()
    .append("g")
    .attr("class", "pie");


  arc = d3.arc()
    .outerRadius(radius)
    .innerRadius(0);

  pieGroup.append("path")
    .attr("d", arc)
    .attr("fill", function(d) { return color(d.index) })
    .attr("opacity", 0.75)
    .attr("stroke", "white");

  // 6. pieチャートテキストSVG要素の設定
  var text = d3.arc()
    .outerRadius(radius - 30)
    .innerRadius(radius - 30);


  pieGroup.append("text")
    .attr("fill", "white")
    .attr("transform", function(d) { return "translate(" + text.centroid(d) + ")"; })
    .attr("dy", "5px")
    .attr("font", "10px")
    .attr("font-size", "15px")
    .attr("text-anchor", "middle")
    .text(function(d) { return d.data.name; });



}
