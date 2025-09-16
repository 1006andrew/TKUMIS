import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './header.html',
  styleUrls: ['./header.css']
})
export class HeaderComponent {
  logo = 'src/assets/logo.jpg'; // 把你上傳的圖片放到 src/assets/logo.png
  userName = '王小明';      // 之後可改從 AuthService 拿
}
