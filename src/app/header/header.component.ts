import { Component, EventEmitter, Output, ViewChild } from '@angular/core';
import { MatFormField } from '@angular/material/form-field';
import { MatSelect } from '@angular/material/select';
import  {MatIcon} from '@angular/material/icon'
import { SidenavComponent } from '../sidenav/sidenav.component';
import { PresetOptionsComponent } from '../preset-options/preset-options.component';
import { Router } from '@angular/router';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    MatFormField,
    MatSelect,
    SidenavComponent,
    MatIcon,
    PresetOptionsComponent
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

  handleLogout(){
    sessionStorage.removeItem('user')
    this.router.navigate(['/login'])
  }

}

