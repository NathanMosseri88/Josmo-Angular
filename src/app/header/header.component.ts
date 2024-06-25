import { Component, EventEmitter, Output, ViewChild } from '@angular/core';
import { MatFormField } from '@angular/material/form-field';
import { MatSelect } from '@angular/material/select';
import  {MatIcon} from '@angular/material/icon'
import { SidenavComponent } from '../sidenav/sidenav.component';
import { PresetOptionsComponent } from '../preset-options/preset-options.component';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatToolbar, MatToolbarRow } from '@angular/material/toolbar';
import { AuthService } from '../services/auth.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    CommonModule,
    MatFormField,
    MatSelect,
    SidenavComponent,
    MatIcon,
    PresetOptionsComponent,
    MatButtonModule,
    MatToolbar,
    MatToolbarRow,
    RouterLink,
    RouterLinkActive,
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})

export class HeaderComponent {

  constructor(private router: Router, private authService:AuthService) {}

  @ViewChild(SidenavComponent) sidenav!: SidenavComponent
  
  onToggleSidebar(){
    this.sidenav.toggleSideBar()
  }

  handleLogout(){ // triggered when clicking 'Log Out' button 
    // removes user's auth token from browser's session storage
    sessionStorage.removeItem('user')
    // sends user back to login page
    this.router.navigate(['/login'])
  }

  handleLoginButton(){
    this.router.navigate(['/login'])
  }

  isLoggedIn():boolean {
    return this.authService.isLoggedIn()
  }

  isAdmin() {
    return this.authService.isAdmin
  }

}

