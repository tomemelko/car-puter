
/*
 * GET home page.
 */

exports.index = function(req, res){
  res.render('index', { title: 'Express' });
};

exports.graph = function(req, res){
  var fs = require("fs");
  tempName = req.files.csv.ws.path
  fs.renameSync(tempName, "data.csv");
  res.render('graph', { title: 'Express' });
};

exports.data = function(req, res){
  data = {
    "timeArr" : [],
    "speedArr" : [],
    "rpmArr" : [],
    "accelArr30" : [],
    "accelArr60" : [],
    "gees" : []
  }
  var fs = require("fs");
  var csv = fs.readFileSync("data.csv", {"encoding":"utf-8"});
  var lines = csv.split('\r\n');
  var mostRecentZeroTime = 0;
  var doingAccel = true;

  function gee(t1, t2, s1, s2) {
    return (((s2 - s1) / 3600.0) / ((t2 - t1) / 1000.0))/.006060606;
  }

  var lastTime = 0;
  var lastSpeed = 0;

  for (var i = 0; i < lines.length; i++) {
    var nums = lines[i].split(',');

    if (lines[i] === "")
      continue;

    if (nums[0] === null || nums[1] === null || nums[2] === null)
      continue;

    var time = parseInt(nums[0]);
    var speed = parseFloat(nums[1]);
    var rpm = parseFloat(nums[2]);
    var throttlePos = parseFloat(nums[3]);
    var speedObj = {
      y: speed,
      gearRatio: (rpm/speed)
    };

  	if (speed == 0) {
  		mostRecentZeroTime = time;
  		doingAccel = true;
  	}

  	if (speed > 30 && doingAccel) {
  		data.accelArr30.push(time - mostRecentZeroTime);
  	}

  	if (speed > 60 && doingAccel) {
  		data.accelArr60.push(time - mostRecentZeroTime);
  		doingAccel = false;
  	}

	  data.timeArr.push(parseInt(time/1000));
	  data.speedArr.push(speedObj);
	  data.rpmArr.push(parseFloat(rpm));
    data.gees.push(gee(lastTime, time, lastSpeed, speed));

    lastTime = time;
    lastSpeed = speed;
  };
  res.json(data);
};