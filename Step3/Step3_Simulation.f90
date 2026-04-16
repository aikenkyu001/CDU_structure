program step3_pkgf_sweep
    ! ============================================
    ! Step 3: 改訂版・生成型デジタル PKGF シミュレーション (Fortran版・自律型)
    ! 目的：LAPACKに依存せず、ノルム比による動的次元推定でスイープを実行
    ! ============================================
    implicit none
    integer, parameter :: N = 100
    integer, parameter :: STEPS = 150
    real, parameter :: ETA = 0.25
    
    real, dimension(N, N) :: K, Omega, K_d, Commutator, raw_stim
    real :: blur_sigma, noise_level
    real :: initial_rank, final_rank, jump
    real, dimension(3) :: blurs = (/0.5, 1.5, 3.0/)
    real, dimension(3) :: noises = (/0.01, 0.05, 0.15/)
    integer :: ib, in, t
    
    print *, "Starting Automated Parameter Sweep for Step 3 (Fortran/Self-contained)..."
    
    open(10, file='Step3/simulation_results_fortran.json', status='replace')
    write(10, '(A)') '['

    do ib = 1, 3
        blur_sigma = blurs(ib)
        do in = 1, 3
            noise_level = noises(in)
            
            ! 初期並行鍵
            K = 0.01
            initial_rank = get_effective_rank(K)
            
            do t = 1, STEPS
                ! 1. 刺激生成
                call generate_stimulus(t, raw_stim)
                ! 2. 環境影響 (ボケとノイズ)
                call apply_environment(raw_stim, blur_sigma, noise_level, Omega)
                
                ! 3. PKGF 統一方程式
                call apply_blur(K, 0.8, K_d)
                Commutator = matmul(Omega, K) - matmul(K, Omega)
                K = K_d + ETA * Commutator
                
                ! 4. 非線形増幅と正規化 (U4 ゲージ破れ)
                K = exp(K * 2.0)
                K = K / (sqrt(sum(K**2)) + 1e-12) * 10.0
            end do
            
            final_rank = get_effective_rank(K)
            jump = final_rank - initial_rank
            
            print '(A,F4.1,A,F5.2,A,F9.4)', "Blur: ", blur_sigma, ", Noise: ", noise_level, " -> Rank Jump: ", jump
            
            write(10, '(A)') '  {'
            write(10, '(A,F6.2,A)') '    "blur": ', blur_sigma, ','
            write(10, '(A,F6.2,A)') '    "noise": ', noise_level, ','
            write(10, '(A,F10.6,A)') '    "jump": ', jump, ','
            write(10, '(A,F10.6)') '    "final_rank": ', final_rank
            if (ib == 3 .and. in == 3) then
                write(10, '(A)') '  }'
            else
                write(10, '(A)') '  },'
            end if
        end do
    end do

    write(10, '(A)') ']'
    close(10)
    print *, "Sweep complete. Results saved to Step3/simulation_results_fortran.json"

contains

    subroutine generate_stimulus(t, stim)
        integer, intent(in) :: t
        real, dimension(N, N), intent(out) :: stim
        integer :: cx, cy, r2, i, j
        stim = 0.0
        cx = N/2 + int(N/4 * cos(real(t)/15.0))
        cy = N/2 + int(N/4 * sin(real(t)/15.0))
        r2 = (N/8)**2
        do i = 1, N
            do j = 1, N
                if ((i-cx)**2 + (j-cy)**2 <= r2) stim(i,j) = 1.0
            end do
        end do
    end subroutine generate_stimulus

    subroutine apply_environment(in_mat, sigma, noise, out_mat)
        real, dimension(N, N), intent(in) :: in_mat
        real, intent(in) :: sigma, noise
        real, dimension(N, N), intent(out) :: out_mat
        real, dimension(N, N) :: blurred, r_noise
        call apply_blur(in_mat, sigma, blurred)
        call random_number(r_noise)
        out_mat = blurred + (r_noise - 0.5) * 2.0 * noise
        where (out_mat < 0.0) out_mat = 0.0
        where (out_mat > 1.0) out_mat = 1.0
    end subroutine apply_environment

    subroutine apply_blur(in_mat, sigma, out_mat)
        real, dimension(N, N), intent(in) :: in_mat
        real, intent(in) :: sigma
        real, dimension(N, N), intent(out) :: out_mat
        integer :: i, j
        out_mat = in_mat
        if (sigma < 0.1) return
        do i = 2, N-1
            do j = 2, N-1
                out_mat(i,j) = (in_mat(i-1,j) + in_mat(i+1,j) + in_mat(i,j-1) + in_mat(i,j+1) + in_mat(i,j)*4.0) / 8.0
            end do
        end do
    end subroutine apply_blur

    function get_effective_rank(mat) result(r)
        ! ノルム比による簡易的な動的次元 (Effective Dimension) の推定
        real, dimension(N, N), intent(in) :: mat
        real :: r
        r = sum(mat**2) / (maxval(mat**2) + 1e-12)
    end function get_effective_rank

end program step3_pkgf_sweep
