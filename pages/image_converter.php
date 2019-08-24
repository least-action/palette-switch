<!DOCTYPE html>
<html>

<head>
	<Title>Palette Switch</Title>
</head>

<!--TODO
done
-->

<body>
	<p><a href="./index.html">Home</a></p>

	<form action="./run_image_converter.php" method="post" enctype="multipart/form-data">
		<p>prefix:
			<input type="text" name="prefix" size="60" maxlength="32" 
				placeholder="names of new images will be (prefix)_00.png, (prefix)_01.png .. " required="required" />
		</p>

		<p>files:
			<input id="file_input" type="file" name="images[]" multiple required="required"
				onchange="checkNumOfFiles();"/>
		</p>

		<p id="color_input">palette:
			<!--<input type="color" name="colors_00" required="required" />-->
		</p>
		<button type="button" onclick="addColor();">add color</button>

<!--		<p>Test: <input type="checkbox" name="is_test" checked="checked" /> </p>-->
<!--		<p> <input type="hidden" name="MAX_FILE_SIZE" value="1" /> </p>-->
		<p> <input type="submit" value="convert"/> </p>
	</form>

	<script type="text/javascript">
		var addColor = function()
		{
			var colorNode = document.getElementById("color_input");
			var count = colorNode.childElementCount;

			if (count > 4)
			{
				alert("You cannot select colors more than 5!!");
				return;
			};

			var newNode = document.createElement("input");
			var attType = document.createAttribute("type");
			attType.value = "color";
			newNode.setAttributeNode(attType);
			var attName = document.createAttribute("name");
			attName.value = "colors[" + count + "]";
			newNode.setAttributeNode(attName);
			var attReq = document.createAttribute("required");
			attReq.value = "required";
			newNode.setAttributeNode(attReq);

			colorNode.appendChild(newNode);
		};

		var checkNumOfFiles = function()
		{
			var fileNode = document.getElementById("file_input");

			if (fileNode.files.length > 5)
			{
				alert("You cannot select files more than 5!!");
				fileNode.value="";
			};
		};

		
	</script>
</body>

</html>




















