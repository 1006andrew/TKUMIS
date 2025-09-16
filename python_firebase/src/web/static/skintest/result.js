document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("uploadForm");
    const fileInput = document.getElementById("fileInput");
    const preview = document.getElementById("preview");
    const resultDiv = document.getElementById("result");
  
    const oilLabel = document.getElementById("oilLabel");
    const oilProb = document.getElementById("oilProb");
    const sensiLabel = document.getElementById("sensiLabel");
    const sensiProb = document.getElementById("sensiProb");
  
    // 圖片預覽
    fileInput.addEventListener("change", () => {
      const file = fileInput.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = e => {
          preview.src = e.target.result;
          preview.classList.remove("hidden");
        };
        reader.readAsDataURL(file);
      }
    });
  
    // 表單提交 → 呼叫 API
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
  
      const file = fileInput.files[0];
      if (!file) {
        alert("請選擇一張圖片！");
        return;
      }
  
      const formData = new FormData();
      formData.append("file", file);
  
      try {
        const response = await fetch("/skintest/analyze", {
          method: "POST",
          body: formData,
        });
  
        const data = await response.json();
  
        if (data.error) {
          alert("分析失敗：" + data.error);
          return;
        }
  
        oilLabel.textContent = data.oil_label;
        oilProb.textContent = data.oil_prob.toFixed(4);
        sensiLabel.textContent = data.sensi_label;
        sensiProb.textContent = data.sensi_prob.toFixed(4);
  
        resultDiv.classList.remove("hidden");
      } catch (err) {
        alert("API 請求失敗：" + err.message);
      }
    });
  });
  