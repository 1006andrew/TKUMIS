import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chatbot.html',
  styleUrls: ['./chatbot.css']
})
export class ChatbotComponent {
  question: string = '';
  messages: { role: 'user' | 'bot', text: string }[] = [];
  loading: boolean = false;

  private apiUrl = 'http://localhost:8000/api/chat'; // 後端 FastAPI

  constructor(private http: HttpClient) {}

  sendQuestion() {
    if (!this.question.trim()) return;

    const q = this.question.trim();
    this.messages.push({ role: 'user', text: q });
    this.question = '';
    this.loading = true;

    this.http.post<{ answer: string }>(this.apiUrl, { question: q })
      .subscribe({
        next: (res) => {
          this.messages.push({ role: 'bot', text: res.answer });
          this.loading = false;
        },
        error: (err) => {
          this.messages.push({ role: 'bot', text: `⚠️ 錯誤：${err.message}` });
          this.loading = false;
        }
      });
  }
}
