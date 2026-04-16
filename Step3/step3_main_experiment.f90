program step3_main_experiment
    ! ============================================
    ! Step 3: Optical V-PCM 本実験 (Fortran版)
    ! Python版 step3_pkgf_digital_sim.py と同一のパラメータで実行
    ! ============================================
    implicit none
    integer, parameter :: N = 100
    integer, parameter :: STEPS = 200
    real, parameter :: ETA = 0.15
    real, parameter :: NOISE_LEVEL = 0.02
    
    real, dimension(N, N) :: K, Omega, K_d, Commutator, raw_stim
    real :: current_rank, prev_rank
    integer :: t, i, j
    character(len=20) :: action
    
    print *, "Starting Step 3 Main Experiment (Fortran Implementation)"
    print '(A6,A3,A12,A3,A15)', "Step", "|", "Eff. Rank", "|", "Action"
    print '(A40)', "----------------------------------------"
    
    ! --- 初期化 (Axiom A3) ---
    call random_seed()
    call random_number(K)
    prev_rank = 0.0
    
    ! 結果保存用ファイルのオープン
    open(10, file='Step3/main_experiment_results_fortran.json', status='replace')
    write(10, '(A)') '{'
    write(10, '(A)') '  "ranks": ['

    do t = 0, STEPS - 1
        ! 1. 刺激生成 (動く円)
        call generate_stimulus(t, raw_stim)
        
        ! 2. 環境フィルタ (ボケとノイズ: Axiom D1)
        call apply_physical_filter(raw_stim, Omega)
        
        ! 3. PKGF 統一方程式 (Axiom U3)
        ! 内部散逸 (D)
        call apply_gaussian_blur(K, K_d)
        
        ! 構築 (C): [Omega, K]
        Commutator = matmul(Omega, K) - matmul(K, Omega)
        K = K_d + ETA * Commutator
        
        ! エネルギー保存 (ノルム正規化)
        K = K / (sqrt(sum(K**2)) + 1e-12) * 10.0
        
        ! 4. 指標の計測
        current_rank = calculate_rank_proxy(K)
        
        action = ""
        if (t > 0 .and. abs(current_rank - prev_rank) > 0.5) then
            action = "!! RANK JUMP !!"
        end if
        
        if (mod(t, 20) == 0 .or. action /= "") then
            print '(I6,A3,F12.4,A3,A15)', t, "|", current_rank, "|", action
        end if
        
        ! JSONへの書き出し
        if (t < STEPS - 1) then
            write(10, '(F10.6,A)') current_rank, ','
        else
            write(10, '(F10.6)') current_rank
        end if
        
        prev_rank = current_rank
    end do
    
    write(10, '(A)') '  ]'
    write(10, '(A)') '}'
    close(10)
    
    print '(A40)', "----------------------------------------"
    print *, "Experiment complete. Results saved to Step3/main_experiment_results_fortran.json"

contains

    subroutine generate_stimulus(t, stim)
        integer, intent(in) :: t
        real, dimension(N, N), intent(out) :: stim
        integer :: cx, cy, r2, i, j
        stim = 0.0
        ! 格子模様
        do i = 1, N, 10
            stim(i, :) = 0.5
            stim(:, i) = 0.5
        end do
        ! 動く円
        cx = 50 + int(20.0 * cos(real(t)/10.0))
        cy = 50 + int(20.0 * sin(real(t)/10.0))
        r2 = 15**2
        do i = 1, N
            do j = 1, N
                if ((i-cx)**2 + (j-cy)**2 <= r2) stim(i,j) = 1.0
            end do
        end do
    end subroutine generate_stimulus

    subroutine apply_physical_filter(in_mat, out_mat)
        real, dimension(N, N), intent(in) :: in_mat
        real, dimension(N, N), intent(out) :: out_mat
        real, dimension(N, N) :: blurred, noise
        call apply_gaussian_blur(in_mat, blurred)
        call random_number(noise)
        out_mat = blurred + (noise - 0.5) * 2.0 * NOISE_LEVEL
    end subroutine apply_physical_filter

    subroutine apply_gaussian_blur(in_mat, out_mat)
        real, dimension(N, N), intent(in) :: in_mat
        real, dimension(N, N), intent(out) :: out_mat
        integer :: i, j
        ! 3x3 ガウシアン近似フィルタ
        out_mat = in_mat
        do i = 2, N-1
            do j = 2, N-1
                out_mat(i,j) = (in_mat(i-1,j-1) + in_mat(i-1,j+1) + in_mat(i+1,j-1) + in_mat(i+1,j+1) + &
                                (in_mat(i-1,j) + in_mat(i+1,j) + in_mat(i,j-1) + in_mat(i,j+1))*2.0 + &
                                in_mat(i,j)*4.0) / 16.0
            end do
        end do
    end subroutine apply_gaussian_blur

    function calculate_rank_proxy(mat) result(r)
        real, dimension(N, N), intent(in) :: mat
        real :: r
        ! 動的次元の代替指標 (ノルム比)
        r = sum(mat**2) / (maxval(mat**2) + 1e-12)
    end function calculate_rank_proxy

end program step3_main_experiment
