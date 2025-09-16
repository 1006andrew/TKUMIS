import { Component, signal } from '@angular/core';
import { RouterOutlet, RouterLink, RouterModule } from '@angular/router';
import { NavbarComponent } from './site/shared/navbar/navbar';
import { HeaderComponent } from "./site/shared/header/header";

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterModule, NavbarComponent, ], // RouterLink, HeaderComponent
  templateUrl: './app.html',
  styleUrl: './app.css'
})

export class App {
  protected readonly title = signal('angular_minimal_project_v1_1');
}
