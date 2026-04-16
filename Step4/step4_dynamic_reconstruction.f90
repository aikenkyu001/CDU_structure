program step4_fortran_dynamic
    ! ============================================
    ! Task K: Fortran による極限動的再構成
    ! 目的：CPU 性能をフルに引き出し、100ステップの PKGF サイクルを最速化する
    ! ============================================
    implicit none
    integer, parameter :: N = 256
    integer, parameter :: STEPS = 100
    real, parameter :: DT = 0.05
    real, parameter :: LAMBDA = 0.1
    
    real, dimension(N, N) :: Omega, K, Comm, K_next
    real :: start_t, end_t, total_ms
    integer :: t, i, j
    
    print *, "--- Task K: Fortran Dynamic Reconstruction Benchmark (N=256) ---"
    
    ! 1. 初期化
    call random_seed()
    call random_number(Omega)
    call random_number(K)
    K = K * 0.1
    
    ! 2. 計測開始
    call cpu_time(start_t)
    
    do t = 1, STEPS
        ! Axiom U3: [Omega, K] = Omega K - K Omega
        Comm = matmul(Omega, K) - matmul(K, Omega)
        
        ! 更新: K = K + DT * (Comm - LAMBDA * K)
        K = K + DT * (Comm - LAMBDA * K)
        
        ! 非線形シグモイド活性化 (U4: ゲージ破れ)
        ! exp 関数を要素ごとに適用
        do i = 1, N
            do j = 1, N
                K(i,j) = 1.0 / (1.0 + exp(-K(i,j) * 2.5))
            end do
        end do
    end do
    
    call cpu_time(end_t)
    
    total_ms = (end_t - start_t) * 1000.0
    
    print '(A,F15.4,A)', "  Fortran 100-Step Time: ", total_ms, " ms"
    print '(A,F15.4,A)', "  Avg per Step:         ", total_ms / real(STEPS), " ms"
    print '(A)', "-------------------------------------------------------"
    
    ! 結果の簡易 JSON 出力
    open(10, file='Step4/task_k_fortran_results.json', status='replace')
    write(10, '(A)') '{'
    write(10, '(A,I5,A)')    '  "N": ', N, ','
    write(10, '(A,F15.4)')   '  "fortran_ms": ', total_ms
    write(10, '(A)') '}'
    close(10)

end program step4_fortran_dynamic
