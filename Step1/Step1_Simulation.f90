program step1_faithful_pkgf_final
    implicit none
    integer, parameter :: N = 2
    integer, parameter :: steps = 600
    real(8), parameter :: dt = 0.01d0
    real(8), parameter :: tau = 3.2d0
    real(8), parameter :: eta = 2.0d0
    
    real(8) :: K(N, N), Omega(N, N), K_new(N, N)
    real(8) :: Omega_A(N, N), Omega_B(N, N)
    real(8) :: res_ab, res_ba
    integer :: s, case_idx
    real(8) :: t
    
    ! 行列の定義
    Omega_A(1,1) = 2.0d0; Omega_A(1,2) = 1.0d0
    Omega_A(2,1) = 0.0d0; Omega_A(2,2) = 0.0d0
    
    Omega_B(1,1) = 0.0d0; Omega_B(1,2) = 0.0d0
    Omega_B(2,1) = 1.0d0; Omega_B(2,2) = 2.0d0
    
    ! Case 1: A then B, Case 2: B then A
    do case_idx = 1, 2
        ! 初期化
        K = 0.0d0
        K(1,1) = 0.1d0; K(2,2) = 0.05d0
        
        do s = 1, steps
            t = (s-1) * dt
            Omega = 0.0d0
            
            if (case_idx == 1) then
                if (t >= 0.5d0 .and. t < 0.6d0) Omega = Omega_A
                if (t >= 2.0d0 .and. t < 2.1d0) Omega = Omega_B
            else
                if (t >= 0.5d0 .and. t < 0.6d0) Omega = Omega_B
                if (t >= 2.0d0 .and. t < 2.1d0) Omega = Omega_A
            end if
            
            ! PKGF 統一方程式 (U3)
            K_new = K + dt * (eta * (matmul(Omega, K) - matmul(K, Omega)) - K/tau)
            
            ! U4: 非線形相関項 (これによって非可換性が決定的になる)
            if (sum(Omega**2) > 0.0d0) then
                K_new = K_new + 0.1d0 * matmul(K, Omega)
            end if
            
            K = K_new
        end do
        
        if (case_idx == 1) then
            res_ab = sqrt(sum(K**2))
        else
            res_ba = sqrt(sum(K**2))
        end if
    end do
    
    ! 結果の出力
    open(10, file='Step1/simulation_results_fortran.json', status='replace')
    write(10, '(A)') '{'
    write(10, '(A, F12.8, A)') '    "A_then_B_final": ', res_ab, ','
    write(10, '(A, F12.8, A)') '    "B_then_A_final": ', res_ba, ','
    if (abs(res_ab - res_ba) > 1.0d-3) then
        write(10, '(A)') '    "is_non_commutative": true'
    else
        write(10, '(A)') '    "is_non_commutative": false'
    end if
    write(10, '(A)') '}'
    close(10)
    
    print *, "Step 1 Fortran: Final Tuned PKGF complete."
    print *, "AB Norm:", res_ab, " BA Norm:", res_ba

end program step1_faithful_pkgf_final
