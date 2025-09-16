// import { Component, inject } from '@angular/core';
// import { RouterModule } from '@angular/router';
// import { CommonModule } from '@angular/common';
// import { AuthService } from '../../../service/auth';
// import { HttpClient } from '@angular/common/http';
// import { FormsModule } from '@angular/forms';


// @Component({
//   selector: 'app-navbar',
//   standalone: true,
//   imports: [CommonModule, RouterModule,FormsModule],
//   templateUrl: './navbar.html',
//   styleUrls: ['./navbar.css'],
// })
// export class NavbarComponent {
//   auth = inject(AuthService);
//   chatbotOpen = false;
//   question: string = '';
//   messages: { role: 'user' | 'bot'; text: string }[] = [];
//   loading = false;

//   private apiUrl = 'http://localhost:8000/api/chat';

//   constructor(private http: HttpClient) {}

//   toggleChatbot() {
//     this.chatbotOpen = !this.chatbotOpen;
//   }

//   sendQuestion() {
//     if (!this.question.trim()) return;

//     const q = this.question.trim();
//     this.messages.push({ role: 'user', text: q });
//     this.question = '';
//     this.loading = true;

//     this.http.post<{ answer: string }>(this.apiUrl, { question: q }).subscribe({
//       next: (res) => {
//         this.messages.push({ role: 'bot', text: res.answer });
//         this.loading = false;
//       },
//       error: (err) => {
//         this.messages.push({ role: 'bot', text: `⚠️ 錯誤：${err.message}` });
//         this.loading = false;
//       },
//     });
//   }
// }

import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { HttpClient } from '@angular/common/http';
import { AuthService } from '../../../service/auth';


@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './navbar.html',
  styleUrls: ['./navbar.css']
})
export class NavbarComponent {
  logo = 'assets/logo.jpg';     // NB Logo 圖片（放到 src/assets/logo.png）
  auth = inject(AuthService);
  chatbotOpen = false;
  question = '';
  loading = false;
  messages: { role: 'user' | 'bot'; text: string }[] = [];

  constructor(private http: HttpClient) {}

  toggleChatbot() {
    this.chatbotOpen = !this.chatbotOpen;
  }

  async sendQuestion() {
    if (!this.question.trim()) return;
    this.messages.push({ role: 'user', text: this.question });
    const q = this.question;
    this.question = '';
    this.loading = true;
    // 這裡接你的 chatbot 邏輯；先放假回覆
    setTimeout(() => {
      this.messages.push({ role: 'bot', text: `我收到了：「${q}」` });
      this.loading = false;
    }, 500);
  }
}
