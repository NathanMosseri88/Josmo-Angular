import { Component, EventEmitter, Output, ViewChild } from '@angular/core';
import { MatFormField } from '@angular/material/form-field';
import { MatSelect } from '@angular/material/select';
import  {MatIcon} from '@angular/material/icon'
import { SidenavComponent } from '../sidenav/sidenav.component';
import { PresetOptionsComponent } from '../preset-options/preset-options.component';
import { Router } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    MatFormField,
    MatSelect,
    SidenavComponent,
    MatIcon,
    PresetOptionsComponent,
    MatButtonModule
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})

export class HeaderComponent {

  constructor(private router: Router) {}

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

}

