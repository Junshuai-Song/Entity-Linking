// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// This extension demonstrates using chrome.downloads.download() to
// download URLs.

var allLinks = [];
var visibleLinks = [];

function tel() {
    var tel = false;
    try {
        tel = new XMLHttpRequest();
    } catch(e) {
        //针对ie浏览器
        try {
            tel = new ActiveXObject('Msxml2.XMLHTTP');//ie8
        } catch(e) {
            try {
                tel = new ActiveXObject('Microsoft.XMLHTTP');
            } catch(e) {
                alert('你的浏览器不支持ajax');
            }
        }
    }
    return tel;
}

// Display all visible links.
function showLinks() {
  var linksTable = document.getElementById('links');
  while (linksTable.children.length > 1) {
    linksTable.removeChild(linksTable.children[linksTable.children.length - 1])
  }
  
  // 这里处理 visibleLinks ，需要调用分词，在CGI中寻找索引，找到所有的xxx
  // 目前visibleLinks[0]就是我们当前选中的文本
  while(visibleLinks.length>1){
    visibleLink.pop();
  }
  
  var nokia = tel();
  nokia.open('GET','http://192.9.200.67:8088/cgi-bin/search.pl?content=' + visibleLinks[0],false);
  nokia.onreadystatechange = function () {
      if(this.readyState==4&&this.status==200) {
          visibleLinks.pop();

	 	  var line = this.responseText;
          var content = line.split(';');
          // 这里处理responseText的内容，赋值给visibleLinks[]数组
          for(var i =0;i<content.length;i++){
		  	visibleLinks.push(content[i]);
		  }
         
      }                                                                                                        //页面上    
  }
  nokia.send(null);
  allLinks = visibleLinks;  // 一开始认为所有的都是需要展示的
  
  for (var i = 0; i < visibleLinks.length; ++i) {
    var row = document.createElement('tr');
    var col0 = document.createElement('td');
    var col1 = document.createElement('td');
    var col2 = document.createElement('td');
    var checkbox = document.createElement('input');
    checkbox.checked = true;
    checkbox.type = 'checkbox';
    checkbox.id = 'check' + i;
    col0.appendChild(checkbox);
    
    col2.innerText = visibleLinks[i];   // 这里是增加内容的
    col2.style.whiteSpace = 'nowrap';
    col2.onclick = function() {
      checkbox.checked = !checkbox.checked;
    }
    row.appendChild(col0);
//    row.appendChild(col1);
    row.appendChild(col2);
    linksTable.appendChild(row);
  }
}

function showLinks_filter() {
// 筛选的show，不重新请求
  var linksTable = document.getElementById('links');
  while (linksTable.children.length > 1) {
    linksTable.removeChild(linksTable.children[linksTable.children.length - 1])
  }
  
  
  for (var i = 0; i < visibleLinks.length; ++i) {
    var row = document.createElement('tr');
    var col0 = document.createElement('td');
    var col1 = document.createElement('td');
    var col2 = document.createElement('td');
    var checkbox = document.createElement('input');
    checkbox.checked = true;
    checkbox.type = 'checkbox';
    checkbox.id = 'check' + i;
    col0.appendChild(checkbox);
    
    col2.innerText = visibleLinks[i];   // 这里是增加内容的
    col2.style.whiteSpace = 'nowrap';
    col2.onclick = function() {
      checkbox.checked = !checkbox.checked;
    }
    row.appendChild(col0);
//    row.appendChild(col1);
    row.appendChild(col2);
    linksTable.appendChild(row);
  }
}



// Toggle the checked state of all visible links.
function toggleAll() {
  var checked = document.getElementById('toggle_all').checked;
  for (var i = 0; i < visibleLinks.length; ++i) {
    document.getElementById('check' + i).checked = checked;
  }
}


// Download all visible checked links.
function downloadCheckedLinks() {
  for (var i = 0; i < visibleLinks.length; ++i) {
    if (document.getElementById('check' + i).checked) {
      chrome.downloads.download({url: "https://www.baidu.com",
                                 conflictAction: 'uniquify',
                                 saveAs: false},
           function(id) {
      });
    }
  }
  window.close();
}

// Re-filter allLinks into visibleLinks and reshow visibleLinks.
function filterLinks() {
  var filterValue = document.getElementById('filter').value;
  if (document.getElementById('regex').checked) {
    visibleLinks = allLinks.filter(function(link) {
      return link.match(filterValue);
    });
  } else {
    var terms = filterValue.split(' ');
    visibleLinks = allLinks.filter(function(link) {
      for (var termI = 0; termI < terms.length; ++termI) {
        var term = terms[termI];
        if (term.length != 0) {
          var expected = (term[0] != '-');
          if (!expected) {
            term = term.substr(1);
            if (term.length == 0) {
              continue;
            }
          }
          var found = (-1 !== link.indexOf(term));
          if (found != expected) {
            return false;
          }
        }
      }
      return true;
    });
  }
  showLinks_filter();
}

// Add links to allLinks and visibleLinks, sort and show them.  send_links.js is
// injected into all frames of the active tab, so this listener may be called
// multiple times.
chrome.extension.onRequest.addListener(function(links) {
  for (var index in links) {
    allLinks.push(links[index]);
  }
  allLinks.sort();
  visibleLinks = allLinks;
  showLinks();
});

// Set up event handlers and inject send_links.js into all frames in the active
// tab.
window.onload = function() {
  document.getElementById('filter').onkeyup = filterLinks;
  document.getElementById('regex').onchange = filterLinks;
  document.getElementById('toggle_all').onchange = toggleAll;
  document.getElementById('download0').onclick = downloadCheckedLinks;
  document.getElementById('download1').onclick = downloadCheckedLinks;


  chrome.windows.getCurrent(function (currentWindow) {
    chrome.tabs.query({active: true, windowId: currentWindow.id},
                      function(activeTabs) {
      chrome.tabs.executeScript(
        activeTabs[0].id, {file: 'send_links.js', allFrames: true});
    });
  });
};
