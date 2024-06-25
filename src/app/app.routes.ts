import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { NotFoundComponent } from './not-found/not-found.component';
import { ProposalFormComponent } from './proposal-form/proposal-form.component';
import { SignupComponent } from './signup/signup.component';
import { ComparativeStyleComponent } from './comparative-style/comparative-style.component';
import { AuthGuard } from './auth.guard';

export const routes: Routes = [
    {path: 'login', component: LoginComponent},
    {path: 'signup', component: SignupComponent},
    {path: 'proposal-form', component: ProposalFormComponent, canActivate: [AuthGuard]},
    {path: 'styles-report', component: ComparativeStyleComponent, canActivate: [AuthGuard]},
    {path: '', redirectTo: '/proposal-form', pathMatch: 'full'},
    {path: '**', component: NotFoundComponent}
];
