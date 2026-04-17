program step2_faithful_pkgf_final
    implicit none
    integer, parameter :: N = 4
    integer, parameter :: steps = 400
    real(8), parameter :: dt = 0.1d0
    real(8), parameter :: tau = 5.0d0
    real(8), parameter :: eta = 2.0d0
    
    real(8) :: K(N, N), Omega(N, N), K_new(N, N), K_ref(N, N)
    real(8) :: Omega_base(N, N)
    real(8) :: charge_vals(2)
    real(8) :: final_norm, off_diag_norm
    logical :: triggered
    integer :: s, c_idx, i, j
    
    ! ダミーの乱数行列 (Python版 seed 42 と同様の性質を模倣)
    Omega_base = 0.0d0
    do i = 1, N
        do j = 1, N
            Omega_base(i, j) = sin(real(i*j, 8)) * 1.5d0 ! 固定パターン
        end do
    end do
    
    charge_vals = [0.1d0, 9.0d0]
    
    open(10, file='Step2/simulation_results_fortran.json', status='replace')
    write(10, '(A)') '{'
    
    do c_idx = 1, 2
        ! 初期化
        K = 0.0d0
        K(1, 1) = 0.1d0
        K_ref = 0.0d0
        K_ref(1, 1) = 0.1d0
        triggered = .false.
        
        Omega = (charge_vals(c_idx) / 9.0d0) * Omega_base
        
        do s = 1, steps
            ! D: 散逸
            K_new = K + dt * (- (K - K_ref) / tau)
            
            ! C: 構築 (交換子)
            if (s <= 100) then ! t < 10.0
                K_new = K_new + dt * eta * (matmul(Omega, K) - matmul(K, Omega))
            end if
            
            K = K_new
            
            ! U: 非線形相転移 (非対角成分のノルムで判定)
            off_diag_norm = 0.0d0
            do i = 1, N
                do j = 1, N
                    if (i /= j) off_diag_norm = off_diag_norm + K(i, j)**2
                end do
            end do
            off_diag_norm = sqrt(off_diag_norm)
            
            if (off_diag_norm > 0.05d0) then
                triggered = .true.
                K = K + 0.1d0 * dt * tanh(10.0d0 * K)
            end if
        end do
        
        final_norm = sqrt(sum(K**2))
        
        if (c_idx == 1) then
            write(10, '(A, F12.8, A)') '    "charge_0.1uC_norm": ', final_norm, ','
            write(10, '(A, L1, A)') '    "charge_0.1uC_triggered": ', triggered, ','
        else
            write(10, '(A, F12.8, A)') '    "charge_9.0uC_norm": ', final_norm, ','
            write(10, '(A, L1, A)') '    "charge_9.0uC_triggered": ', triggered, ','
            if (triggered .and. .not. (charge_vals(1) > 1.0d0)) then
                 write(10, '(A)') '    "is_9uC_critical": true'
            else
                 write(10, '(A)') '    "is_9uC_critical": false'
            end if
        end if
    end do
    
    write(10, '(A)') '}'
    close(10)
    
    print *, "Step 2 Fortran: Final Tuned PKGF complete."

end program step2_faithful_pkgf_final
