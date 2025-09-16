// src/app/pages/home/home.component.ts
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  templateUrl: './home.html',   // ✅ 改正
  styleUrl: './home.css'        // ✅ 改正
})

export class HomeComponent implements OnInit {
  constructor(private router: Router) {}

  ngOnInit(): void {
    // 進入首頁時，直接導向 book-a-treatment
    this.router.navigate(['/book-a-treatment']);
  }
}
