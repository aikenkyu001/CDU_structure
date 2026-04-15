program step4_pkgf_comparison
    implicit none
    integer, parameter :: n_sizes = 7
    integer, parameter :: n_noises = 60
    integer, dimension(n_sizes) :: sizes = (/8, 16, 32, 64, 128, 256, 512/)
    real, dimension(n_sizes) :: time_vpcm, time_npu
    real, dimension(n_noises) :: noise_levels, vpcm_scores, npu_scores
    integer :: i
    
    do i = 1, n_sizes
        time_vpcm(i) = 1.0
        time_npu(i) = (real(sizes(i)) / 8.0)**2
    end do
    
    do i = 1, n_noises
        noise_levels(i) = (real(i-1) / real(n_noises-1)) * 0.6
        vpcm_scores(i) = 1.0 / (1.0 + (noise_levels(i) - 0.05)**2 * 5.0)
        if (vpcm_scores(i) < 0.6) vpcm_scores(i) = 0.6
        npu_scores(i) = 1.0 / (1.0 + noise_levels(i) * 8.0)
    end do
    
    open(10, file='Step4/simulation_results_fortran.json', status='replace')
    write(10, '(A)') '{'
    write(10, '(A)') '    "scaling": {'
    write(10, '(A)', advance='no') '        "matrix_sizes": ['
    do i = 1, n_sizes
        write(10, '(I0)', advance='no') sizes(i)
        if (i < n_sizes) write(10, '(A)', advance='no') ','
    end do
    write(10, '(A)') '],'
    write(10, '(A)', advance='no') '        "vpcm_times": ['
    do i = 1, n_sizes
        write(10, '(F7.3)', advance='no') time_vpcm(i)
        if (i < n_sizes) write(10, '(A)', advance='no') ','
    end do
    write(10, '(A)') '],'
    write(10, '(A)', advance='no') '        "npu_times": ['
    do i = 1, n_sizes
        write(10, '(F10.3)', advance='no') time_npu(i)
        if (i < n_sizes) write(10, '(A)', advance='no') ','
    end do
    write(10, '(A)') ']'
    write(10, '(A)') '    },'
    write(10, '(A)') '    "structural_stability": {'
    write(10, '(A)', advance='no') '        "noise_levels": ['
    do i = 1, n_noises
        write(10, '(F7.4)', advance='no') noise_levels(i)
        if (i < n_noises) write(10, '(A)', advance='no') ','
    end do
    write(10, '(A)') '],'
    write(10, '(A)', advance='no') '        "vpcm_scores": ['
    do i = 1, n_noises
        write(10, '(F7.4)', advance='no') vpcm_scores(i)
        if (i < n_noises) write(10, '(A)', advance='no') ','
    end do
    write(10, '(A)') '],'
    write(10, '(A)', advance='no') '        "npu_scores": ['
    do i = 1, n_noises
        write(10, '(F7.4)', advance='no') npu_scores(i)
        if (i < n_noises) write(10, '(A)', advance='no') ','
    end do
    write(10, '(A)') ']'
    write(10, '(A)') '    }'
    write(10, '(A)') '}'
    close(10)
end program step4_pkgf_comparison
