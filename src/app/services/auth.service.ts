import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  admin = new BehaviorSubject<boolean>(true)

  constructor() { }

  isLoggedIn(): boolean {
    return !!sessionStorage.getItem('user')
  }

  isAdmin():Observable<boolean> {
    let token = sessionStorage.getItem('admin')
    return this.admin.asObservable()
  }

}
