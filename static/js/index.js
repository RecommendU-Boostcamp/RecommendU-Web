
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
	if (value == 'other') {
		document.getElementById("question_list").style.display='none';
		document.getElementById("question-insert").innerHTML = '<div id="question-input" style="display:flex;"><textarea list="question_list" name="" id="question-text" placeholder="자소서 문항을 입력하세요.(지원동기, 포부 등)" rows="1" cols="30" maxlength="150"></textarea><button class="return-button" onClick="questionReverse();">돌아가기</button><div>'
		document.getElementById("sample-button").style.display='none';
	}
}

function questionReverse() {
	document.getElementById("question-input").remove();
	document.getElementById("question_list").style.display='block';
	document.getElementById("sample-button").style.display='block';
}

function listShow(){
	const no_data = document.getElementById("no-data");
	no_data.classList.add("hide");
	const exist_data = document.getElementById("exist-data");
	exist_data.classList.add("show");
}

function callSmall(large, majorList){
	//  large.value // 지금 선택된 major_large의 이름
	//  majorList // majorLarge를 담은 리스트
	//  majorList[0].major_large // '교육계열'
	//  majorList[0].major_small // 교육계열에 속하는 소분류들

	const majorLarge = majorList.find(function(element) {
		if(element.major_large === large) {
			return true;
		}})

  const majorSmalls = majorLarge.major_small


	const small_elem = document.getElementById('major-small')
	small_elem.replaceChildren()

	for (let i=0;i<majorSmalls.length;i++){
		const temp_small = document.createElement('option')
		temp_small.setAttribute('value', majorSmalls[i]);
		temp_small.innerHTML = majorSmalls[i]
		console.log(temp_small)
		small_elem.appendChild(temp_small)
	}
}