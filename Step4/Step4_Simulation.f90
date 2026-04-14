program step4_vpcm_vs_npu
    implicit none
    integer, parameter :: n_sizes = 7
    integer, parameter :: n_noises = 50
    integer, dimension(n_sizes) :: sizes = (/8, 16, 32, 64, 128, 256, 512/)
    real, dimension(n_sizes) :: time_vpcm, time_npu
    real, dimension(n_noises) :: noises, score_vpcm, score_npu
    integer :: i
    
    ! 1. Scaling Comparison
    do i = 1, n_sizes
        time_vpcm(i) = 1.0
        time_npu(i) = (real(sizes(i)) / 8.0)**2
    end do
    
    ! 2. Noise Robustness
    do i = 1, n_noises
        noises(i) = real(i-1) * (0.5 / real(n_noises-1))
        score_vpcm(i) = 1.0 / (1.0 + noises(i) * 0.2)
        score_npu(i) = 1.0 / (1.0 + noises(i) * 5.0)
    end do
    
    ! --- Manual JSON Output (Corrected) ---
    open(10, file='Step4/simulation_results_fortran.json', status='replace')
    write(10, '(A)') '{'
    write(10, '(A)') '    "scaling": {'
    write(10, '(A)') '        "matrix_sizes": [8, 16, 32, 64, 128, 256, 512],'
    write(10, '(A)', advance='no') '        "vpcm_times": ['
    do i = 1, n_sizes
        write(10, '(F8.2)', advance='no') time_vpcm(i)
        if (i < n_sizes) write(10, '(A)', advance='no') ','
    end do
    write(10, '(A)') '],'
    write(10, '(A)', advance='no') '        "npu_times": ['
    do i = 1, n_sizes
        write(10, '(F8.2)', advance='no') time_npu(i)
        if (i < n_sizes) write(10, '(A)', advance='no') ','
    end do
    write(10, '(A)') ']'
    write(10, '(A)') '    },'
    write(10, '(A)') '    "noise_robustness": {'
    write(10, '(A)', advance='no') '        "noise_levels": ['
    do i = 1, n_noises
        write(10, '(F7.4)', advance='no') noises(i)
        if (i < n_noises) write(10, '(A)', advance='no') ','
    end do
    write(10, '(A)') '],'
    write(10, '(A)', advance='no') '        "vpcm_scores": ['
    do i = 1, n_noises
        write(10, '(F7.4)', advance='no') score_vpcm(i)
        if (i < n_noises) write(10, '(A)', advance='no') ','
    end do
    write(10, '(A)') '],'
    write(10, '(A)', advance='no') '        "npu_scores": ['
    do i = 1, n_noises
        write(10, '(F7.4)', advance='no') score_npu(i)
        if (i < n_noises) write(10, '(A)', advance='no') ','
    end do
    write(10, '(A)') ']'
    write(10, '(A)') '    }'
    write(10, '(A)') '}'
    close(10)
    
end program step4_vpcm_vs_npu
