document.addEventListener("DOMContentLoaded", () => {
    // گرفتن دکمه Add و container یادداشت‌ها
    const addButton = document.getElementById("add");
    const noteCenter = document.getElementById("note-center");

    // مدیریت کلیک روی دکمه Add
    addButton.addEventListener("click", () => {
        // ساخت یک عنصر جدید note-box
        const noteBox = document.createElement("article");
        noteBox.className = "note-box";

        // افزودن محتوای داخلی به note-box
        noteBox.innerHTML = `
            <div class="box-center">
                <div class="note-nav">
                    <h5>time & date</h5>
                </div>
                <form action="#">
                    <div class="title">
                        <input class="inp-title" type="text" placeholder="عنوان">
                    </div>
                    <div class="line"></div>
                    <div class="note-text">
                        <textarea class="txtarea" name="text" placeholder="یادداشت" required></textarea>
                    </div>
                </form>
                <div class="footer-note">
                    <button class="save">
                       <i class="bi bi-floppy"></i>
                    </button>
                    <button class="delete">
                        <i class="bi bi-trash3"></i>
                    </button>
                    <button class="star">
                        <i class="bi bi-star"></i>
                    </button>
                </div>
            </div>
        `;

        // اضافه کردن note-box جدید به note-center
        noteCenter.appendChild(noteBox);

        // افزودن رویداد حذف برای دکمه حذف
        const deleteButton = noteBox.querySelector(".delete");
        deleteButton.addEventListener("click", () => {
            noteBox.remove();
        });
    });
});
