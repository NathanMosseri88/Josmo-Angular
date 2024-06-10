import { Component } from '@angular/core';
import {MatSelectModule} from '@angular/material/select'
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatCardModule} from '@angular/material/card'
import { RouterLink, RouterLinkActive } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatCardModule,
    RouterLink,
    RouterLinkActive,
    MatButtonModule,
    ReactiveFormsModule
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})

export class LoginComponent {

  loginFormData: FormGroup
  constructor(private formBuilder: FormBuilder, private apiService: ApiService) {
    this.loginFormData = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
    });
  }

  handleSubmit(e:any){
    console.log(this.loginFormData.value)
    this.apiService.login(this.loginFormData.value).subscribe(
      res => {
        console.log(res)
        sessionStorage.setItem('user', res.access_token)
        this.loginFormData.reset()
      },
      error => {
        console.log(error)
        alert(error.error.error)
      }
    )
  }
}
