function copyText(name) {
  var preElements = document.getElementsByTagName("pre");
  for (var i = 0; i < preElements.length; i++) {
    if (preElements[i].getAttribute("name") == name) {
      var textToCopy = preElements[i].textContent;
      navigator.clipboard.writeText(textToCopy);
      break;
    }
  }
}
