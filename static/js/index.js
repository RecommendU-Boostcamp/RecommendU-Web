
function popup_open(id) {
	id.classList.add("show");
}
function popup_close(id) {
	id.classList.remove("show");
}

function job_check(content,array,id){
	if (content.checked == true){
		for(i=0; i<array.length; i++){
			const temp = document.createElement("div")
			temp.innerHTML = '<div class="cb"><input type="checkbox" id='+id[i]+' name="job_detail" onClick = "checkSmallOnlyOne(this)"><label for='+id[i]+'><span class="cbText">'+array[i]+'</span></label></div>'
			document.getElementById("job_result").append(temp);
		}
	}
	else{
		document.getElementById("job_result").innerText = "";
	}
}

function checkOnlyOne(element) {
  
	const checkboxes = document.getElementsByName("job_main");
	
	checkboxes.forEach((cb) => {
	  cb.checked = false;
	})
	document.getElementById("job_result").innerText = "";
	element.checked = true;
}

function checkSmallOnlyOne(element) {
  
	const checkboxes = document.getElementsByName("job_detail");
	
	checkboxes.forEach((cb) => {
	  cb.checked = false;
	})
	element.checked = true;
}

function questionDefaultCheck(value) {
	if (value == "other") {
		document.getElementById("question_list").remove();
		document.querySelector(".question").innerHTML = '<textarea list="question_list" name="" id="" placeholder="자소서 문항을 입력하세요.(지원동기, 포부 등)" rows="1" cols="30" maxlength="30"></textarea>'
	}
}