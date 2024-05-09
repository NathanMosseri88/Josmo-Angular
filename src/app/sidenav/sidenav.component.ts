import { Component } from '@angular/core';
import {  RouterLink, RouterLinkActive } from '@angular/router';
import { MatSidenavModule } from '@angular/material/sidenav';
import {MatToolbar} from '@angular/material/toolbar'
import {MatIcon} from '@angular/material/icon'

@Component({
  selector: 'app-sidenav',
  standalone: true,
  imports: [
    MatSidenavModule,
    RouterLink,
    RouterLinkActive,
    MatToolbar,
    MatIcon
  ],
  templateUrl: './sidenav.component.html',
  styleUrl: './sidenav.component.css'
})
export class SidenavComponent {
  opened = false;

  toggleSideBar() {
    this.opened = !this.opened;
  }
}
