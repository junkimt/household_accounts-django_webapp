function showLineGraph (dataset, html_tag, html_class) {

  var width = parseInt(window.innerWidth * 1.0); // グラフの幅
  //var height = parseInt(width * 0.4); // グラフの高さ
  var height = 350
  var margin = { "top": 30, "bottom": 60, "right": 80, "left": 150 };

  var maxYenDefault = 50000
  var maxYenDataset = d3.max(dataset, function(d) { return d[1]; })
  if (maxYenDefault > maxYenDataset){
    maxYenDataset = maxYenDefault;
  }

  // 2. SVG領域の設定
  var selector_str = html_tag + "." + html_class;
  var svg = d3.select(selector_str).append("svg").attr("width", width).attr("height", height);

  // 3. 軸スケールの設定
  /*
  var xScale = d3.scaleLinear()
    .domain([0, d3.max(dataset, function(d) { return d[0]; })])
    .range([margin.left, width - margin.right]);
  */

  var xScale = d3.scaleLinear()
    .domain([0, 31])
    .range([margin.left, width - margin.right]);

  var yScale = d3.scaleLinear()
    .domain([0, maxYenDataset])
    .range([height - margin.bottom, margin.top]);

  // 4. 軸の表示
  var axisx = d3.axisBottom(xScale).ticks(5);
  var axisy = d3.axisLeft(yScale).ticks(5);


  svg.append("g")
    .attr("transform", "translate(" + 0 + "," + (height - margin.bottom) + ")")
    .call(axisx)
    .append("text")
    .attr("fill", "black")
    .attr("x", (width - margin.left - margin.right) / 2 + margin.left)
    .attr("y", 35)
    .attr("text-anchor", "middle")
    .attr("font-size", "10pt")
    .attr("font-weight", "bold")
    .text("日付");


  svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + 0 + ")")
    .call(axisy)
    .append("text")
    .attr("fill", "black")
    .attr("text-anchor", "middle")
    .attr("x", -(height - margin.top - margin.bottom) / 2 - margin.top)
    .attr("y", -60)
    .attr("transform", "rotate(-90)")
    .attr("font-weight", "bold")
    .attr("font-size", "10pt")
    .text("１日ごとの使用金額の合計");

  // 5. ラインの表示
  svg.append("path")
    .datum(dataset)
    .attr("fill", "none")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 1.5)
    .attr("d", d3.line()
      .x(function(d) { return xScale(d[0]); })
      .y(function(d) { return yScale(d[1]); }));


}
