// Sidebar
var sidebar_is_shown = false;
var open = true
var filled = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

// Sections
$('page .page-header ul li').click(function () {
  if ($(this).hasClass('disabled'))
    return;
  var page = $(this).parent().parent().parent();
  $('section.active', page).removeClass('active');
  $('.page-header ul li', page).removeClass('active');
  $('section#' + $(this).data('target-section'), page).addClass('active');
  $(this).addClass('active');
  $('.page-header span', page).html($(this).html());
  $('section#' + $(this).data('target-section'), page).trigger('load');
})

function openModal(id) {
  // dailog.show(); 
  var dailog = document.getElementById(id);
  dailog.showModal();
}

function closeModal(id) {
  var dailog = document.getElementById(id);
  dailog.close();
}
//button
$('section#out button').click(function () {
  var button = $(this).parent().parent().parent();
  $('button.active', button).addClass(' ');
  $('button.active', button).removeClass('active');
  $('button#' + $(this).data('target-section'), button).addClass('active');
  $(this).addClass('active');
  $('.feedback').html('');
})

// Forms
jQuery.fn.extend({
  disable: function (state) {
    return this.each(function () {
      this.disabled = state;
    });
  }
});

function clearForm(form) {
  $('input[type="text"], input[type="number"], select', form).val('');
  $('input[type="radio"]', form).prop('checked', false);
  $('input[type="checkbox"]', form).prop('checked', false);
  $('textarea', form).val('');
  $('input[name="action"]').val('insert');
  Currently_edit = 0;
  return;
}

$("form").submit(function (e) {
  var form = $(this);
  var request = {
    url: form.attr('action'),
    type: form.attr('method'),
    data: form.serialize(),
    success: function (response) {
      $('.feedback', form).html(response);
    },
    error: function () {
      $('.feedback', form).html('<span class="error">Unexpected error or server is down</span>');
    },
    complete: function (jqXHR, textStatus) {
      clearForm(form);
      $('input, textarea, select, button', form).disable(false);
      $('input', form).eq(0).focus();

      if ($('page#pharmacy').hasClass('active') && $('section#patients').hasClass('active')) {
        filled = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        $('page#pharmacy section#patients input[name="action"]').val('insert');
        $('page#pharmacy section#patients tbody').html('<tr><td><select id="drugs-0" name="drugs-0" autocomplete="on" onclick="fill(0)"></select></td><td><input type="number" name="qty-0" autocomplete="off"></td><!--<td><button type="button" class="btn btn-success btn-sm" onclick="dispense(this)"><i class="fa fa-check"></i></button></td></tr>');
        $('page#pharmacy section#patients table select').on('input', pharmacyCheckDrugs);
        $('#ph_patients_feedback').html('');
        $('input#ph_code').focus();
      }
    }
  }
  $('.feedback', form).html('<div class="loader"><div class="scanner"><span>Loading...</span></div></div>');
  $('input, textarea, select, button', form).disable(true);
  $.ajax(request);
  return false;
});
function update_centrifuge_value(lab_code, value) {
  var checked = document.getElementById("check-" + lab_code).checked;
  var refresh = true;
  if (!checked) {
    var locked = document.getElementById("lock-" + lab_code).checked;
    if (locked) {
      document.getElementById("check-" + lab_code).checked = true;
      return;
    }
    else {
      refresh = false;
      document.getElementById("increment-" + lab_code).style.visibility = "visible";
      document.getElementById("decrement-" + lab_code).style.visibility = "visible";
      document.getElementById("tubes-" + lab_code).disabled =false;
      document.getElementById("tubes-" + lab_code).setAttribute("min", 0);
    }
  }
  setTimeout(function () {
    $.ajax({
      url: '/blood/centrifuge',
      type: 'GET',
      data: { 'lab_code': lab_code, 'value': value },
      success: function (response) {
        $('section#out div span.feedback').html(response);
        if (!response.includes("Error")) {
          if (refresh)
            refreshCentrifuge()
        }
      },
      error: function (response) {
        $('section#out div span.feedback').html(response);
      },
    });
  }, 200)

}
function update_value(lab_code, value, filter) {
  if (value === "")
    alert("please fill the value of lab code (" + lab_code + ") first");
  else {
    setTimeout(function () {
      $.ajax({
        url: '/blood/out',
        type: 'GET',
        data: { 'filter': filter, 'lab_code': lab_code, 'value': value },
        success: function (response) {
          $('section#out div span.feedback').html(response);
          if (!response.includes("Error")) {
            q = "row-" + lab_code
            document.getElementById(q).innerText = ''
          }
        },
        error: function (response) {
          $('section#out div span.feedback').html(response);
        },
      });
    }, 0);
  }
}
function filter(filter) {
  $('page#blood section#out table#data tbody').html('');
  $('section#out div span.feedback').html('<div class="loader"><div class="scanner"><span>Loading...</span></div></div>');
  $.ajax({
    url: '/blood/filter',
    type: 'GET',
    data: { 'filter': filter },
    success: function (response) {
      var count = 0;
      data = JSON.parse(unescape(response));
      data.forEach(function (x) {
        count += 1;
        lab_code = x[00];
        if (filter === 'CBC') {
          row =
            `<tr id=row-` + lab_code + `  >
              <td>
                <form class="form-out" id="upload-file-` + lab_code + `" method="post" enctype="multipart/form-data">
                  <h3 style=\"margin-left: 10px; min-width:80px\">` + lab_code + `</h3>
                  <input name="lab_code" type="hidden" value="`+ lab_code + `">
                  <input class="form-control form-out-element input left" name="file" type="file">
                  <button class="button form-control form-out-element right" id="upload-file-btn-`+ lab_code + `" onclick="upload('` + lab_code + `')" type="button">Upload</button>
                </form>
              </td>
            </tr>`
        }
        else {
          row = "<tr id=row-" + lab_code + "  ><td><form class=\"form-out\">";
          row += "<h3 style=\"margin-left: 10px; min-width:80px\">" + lab_code + "</h3>"
          row += "<input class=\"form-control form-out-element input left\" id=" + lab_code + " autocomplete=\"off\" type=\"text\" required>";
          row += "<button type=\"button\" class=\"button form-control form-out-element right\" onclick=\"setTimeout(function () {update_value('" + lab_code + "', document.getElementById('" + lab_code + "').value , '" + filter + "')},200)\">update</button>"
          row += "</form></td></tr>"
        }


        $('page#blood section#out table#data tbody').append(row);
      })
      $('section#out div span.feedback').html('');
    },
    error: function () {
      $('section#out div span.feedback').html('<span class="error">Server Error</span>');
    },
  });
}
function refreshBloodSheet() {
  $('page#blood section#sheet table tbody').html('');
  $.ajax({
    url: '/blood/sheet',
    type: 'GET',
    data: '',
    success: function (response) {
      var count = 0;
      data = JSON.parse(unescape(response));
      data.forEach(function (x) {
        count += 1;
        lab_code = x[00];
        sheet_code = x[01];
        in_time = x[02];
        tests = x[04];
        tubes = x[05];
        out_time = x[09];
        hepatitis = x[11];
        cbc = x[12];
        albumin = x[13];
        gpt = x[14];
        pt = x[15];
        bilirubin_direct = x[16];
        bilirubin_total = x[17];
        creatinine = x[18];
        urea = x[19]
        uric = x[20];
        glucose = x[21];
        esr = x[22];
        tag = x[23];
        hba1c = x[24];
        Total_cholesterol = x[25];
        _2Hpp = x[26];
        asot = x[27];
        crp = x[28];
        ldl = x[29];
        hdl = x[30];
        var res = "";
        var show = "";
        var flag = false;
        for (let i = 11; i < 31; i++) {
          if (x[i] != -10 && x[i] != -1) {
            if (i == 11) searchfor = "Hepatitis"
            else if (i == 12) searchfor = "CBC"
            else if (i == 13) searchfor = "Albumin"
            else if (i == 14) searchfor = "GPT"
            else if (i == 15) searchfor = "PT"
            else if (i == 16) searchfor = "Bilirubin_direct"
            else if (i == 17) searchfor = "Bilirubin_total"
            else if (i == 18) searchfor = "Creatinine"
            else if (i == 19) searchfor = "Urea"
            else if (i == 20) searchfor = "Uric"
            else if (i == 21) searchfor = "Glucose"
            else if (i == 22) searchfor = "ESR"
            else if (i == 23) searchfor = "TAG"
            else if (i == 24) searchfor = "HBA1C"
            else if (i == 25) searchfor = "Total_cholesterol"
            else if (i == 26) searchfor = "2Hpp"
            else if (i == 27) searchfor = "ASOT"
            else if (i == 28) searchfor = "CRP"
            else if (i == 29) searchfor = "LDL"
            else if (i == 30) searchfor = "HDL"

            result = tests.indexOf(searchfor)
            res = tests.substring(0, result) + '<span style="color: #6cbe45; font-weight: bold">' + tests.substring(result, result + searchfor.length) + "</span>" + tests.substring(result + searchfor.length);
            tests = res
            flag = true;
          }
        }
        for (let i = 11; i < 31; i++) {
          if (x[i] != -10) {
            if (i == 11) show += "Hepatitis = " + (hepatitis != -1 ? hepatitis : " ") + "\n"
            else if (i == 12) show += "CBC = " + (cbc != -1 ? cbc : " ") + "\n"
            else if (i == 13) show += "Albumin = " + (albumin != -1 ? albumin : " ") + "\n"
            else if (i == 14) show += "GPT = " + (gpt != -1 ? gpt : " ") + "\n"
            else if (i == 15) show += "PT = " + (pt != -1 ? pt : " ") + "\n"
            else if (i == 16) show += "Bilirubin_direct = " + (bilirubin_direct != -1 ? bilirubin_direct : " ") + "\n"
            else if (i == 17) show += "Bilirubin_total = " + (bilirubin_total != -1 ? bilirubin_total : " ") + "\n"
            else if (i == 18) show += "Creatinine = " + (creatinine != -1 ? creatinine : " ") + "\n"
            else if (i == 19) show += "Urea = " + (urea != -1 ? urea : " ") + "\n"
            else if (i == 20) show += "Uric = " + (uric != -1 ? uric : " ") + "\n"
            else if (i == 21) show += "Glucose = " + (glucose != -1 ? glucose : " ") + "\n"
            else if (i == 22) show += "ESR = " + (esr != -1 ? esr : " ") + "\n"
            else if (i == 23) show += "TAG = " + (tag != -1 ? tag : " ") + "\n"
            else if (i == 24) show += "HBA1C = " + (hba1c != -1 ? hba1c : " ") + "\n"
            else if (i == 25) show += "Total_cholesterol = " + (Total_cholesterol != -1 ? Total_cholesterol : " ") + "\n"
            else if (i == 26) show += "2Hpp = " + (_2Hpp != -1 ? _2Hpp : " ") + "\n"
            else if (i == 27) show += "ASOT = " + (asot != -1 ? asot : " ") + "\n"
            else if (i == 28) show += "CRP = " + (crp != -1 ? crp : " ") + "\n"
            else if (i == 29) show += "LDL = " + (ldl != -1 ? lab_code : " ") + "\n"
            else if (i == 30) show += "HDL = " + (hdl != -1 ? hdl : " ") + "\n"

          }
        }
        if (!flag)
          res = tests;

        show += "sheet code = " + sheet_code
        row = '<tr><td>' + count + '</td><td>' + lab_code + '</td><td>' + in_time + '</td><td>' + out_time + '</td><td>' + tubes + '</td><td>' + res + '</td>';
        row += '<td><button style="min-width:60px" onclick="setTimeout(function () {alert(\`' + show + '\`)},300);">results</button></td>';
        row += '<td><button style="' + (cbc != -1 && cbc != -10 ? "visibility: visible;" : "visibility: hidden;") + '" onclick="openModal(\'dialog-' + lab_code + '\')">CBC result</button><dialog id="dialog-' + lab_code + '"><img src="/static/uploads/' + lab_code + '.png" alt="No result yet" height="500" width="500"/><button onclick="closeModal(\'dialog-' + lab_code + '\')" class="right">Close</button></dialog></td></tr>'
        $('page#blood section#sheet table tbody').append(row);
      })
    },
    error: function () {
      alert('Server error');
    },
  });
}
function refreshCentrifuge() {
  $('page#blood section#centrifuge table tbody').html('');
  $.ajax({
    url: '/blood/getcentrifuge',
    type: 'GET',
    data: '',
    success: function (response) {
      data = JSON.parse(unescape(response));
      data.forEach(function (x) {
        row = "";
        lab_code = x[00];
        Date_Centrifuged_timestamp = x[01];
        in_time = x[02];
        tubes = x[05];
        Centrifuged = x[06];
        Date_Centrifuged = x[07];
        out_time = x[09];
        for (let i = 11; i < 31; i++) {
          if (x[i] != -10) {
            if (i == 12 || i == 24 || i == 22)
              continue;
            else {
              console.log(lab_code)
              row += "<tr id=\"" + lab_code + "\"><td><h3>" + lab_code + "</h3></td>";
              row += `<td class="no_border"><button id="decrement-`+ lab_code + `" class="minus" style="font-size:20px;` + (Centrifuged != 0 ? "visibility: hidden;" : " ") + `" type="button" onclick="decrement('tubes-` + lab_code + `')">-</button></td>`;
              row += `<td class="no_border"><input style="padding:0px; display: inline;" class="form-control input" id="tubes-` + lab_code + `" name="tubes-` + lab_code + `" type="number" autocomplete="off" required ` + (Centrifuged != 0 ? "disabled " : " ") + `min="` + tubes + `" value="` + tubes + `"></td>`
              row += `<td class="no_border"><button id="increment-`+ lab_code + `" class="plus" style="font-size: 20px;` + (Centrifuged != 0 ? "visibility: hidden;" : " ") + `" type="button" onclick="increment('tubes-` + lab_code + `')">+</button></td>`
              row += `<td>` + (Date_Centrifuged_timestamp === 0 ? "not yet" : Date_Centrifuged) + `</td>`;
              row += `<td><div class="checkbox-wrapper-31"><input onclick="update_centrifuge_value('` + lab_code + `',document.getElementById('tubes-` + lab_code + `').value)" id=\"check-` + lab_code + `\" name=\"check-` + lab_code + `\" type="checkbox"` + (Centrifuged != 0 ? "checked=\"\"" : " ") + `><svg viewBox="0 0 35.6 35.6"><circle class="background" cx="17.8" cy="17.8" r="17.8"></circle><circle class="stroke" cx="17.8" cy="17.8" r="14.37"></circle><polyline class="check" points="11.78 18.12 15.55 22.23 25.17 12.87"></polyline></svg></div></td>`;
              row += `<td style="padding:0px;"><label class="lock-checkbox">
              <input id="lock-`+ lab_code + `" type="checkbox"` + (Centrifuged != 0 ? "checked=\"\"" : " ") + `>
              <span class="lock-icon">
                <svg viewBox="0 0 24 24">
                  <path d="M12 17c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm6-9h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zM8.9 6c0-1.71 1.39-3.1 3.1-3.1s3.1 1.39 3.1 3.1v2H8.9V6z"></path>
                </svg>
              </span>
            </label>
            </td></tr>`
              $('page#blood section#centrifuge table tbody').append(row);
              break
            }
          }
        }

      })
    },
    error: function (response) {
      alert(response);
    },
  })
}
function increment(id) {

  document.getElementById(id).stepUp();
}
function decrement(id) {
  if (document.getElementById(id).value == 0) {
    document.getElementById(id).value = 0;
    return;
  }
  document.getElementById(id).stepDown();
}
function upload(lab_code) {
  var form_data = new FormData($('#upload-file-' + lab_code)[0]);
  console.log(form_data);
  $.ajax({
    type: 'POST',
    url: '/blood/upload',
    data: form_data,
    contentType: false,
    cache: false,
    processData: false,
    success: function (response) {
      console.log('Success!');
      if (!response.includes("Error")) {
        q = "row-" + lab_code
        document.getElementById(q).innerText = ''
      }
    },
  });

};