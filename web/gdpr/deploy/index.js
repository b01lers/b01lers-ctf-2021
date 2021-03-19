const express = require("express");
var path = require("path");
const app = express();
const port = 3000;

const flag = "bctf{annoying_but_good?}";

var options = {
  root: path.join(__dirname)
};

// .? doesn't work but (2)? works wtf regex
app.get("/*woff(2)?", (req, res) => {
  var url = req.url;
  var file = url.substring(1, url.length);
  console.log("File:", file)
  res.sendFile(file, options, function(err) {
    if (err) {
      next(err);
    } else {
      console.log("Sent:", file);
    }
  });
});

app.get("/", (req, res) => {
  var options = {
    root: path.join(__dirname)
  };
  fileName = "index.html";
  res.sendFile(fileName, options, function(err) {
    if (err) {
      next(err);
    } else {
      console.log("Sent:", fileName);
    }
  });
});

app.get("/flag_policy", (req, res) => {
  res.send(flag);
});

app.listen(port, () => {
  console.log(`Example app listening on ${port}`);
});
