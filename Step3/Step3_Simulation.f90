program step3_vpcm_physics
    implicit none
    integer, parameter :: size = 32
    integer, parameter :: steps = 200
    real, parameter :: noise_lvl = 0.01
    
    real, dimension(size, size) :: K, K_next
    real, dimension(size) :: s_vals
    real :: initial_rank, final_rank, max_rank, rank_jump
    integer :: t, i, j
    
    ! --- Helper: Initialize K with random values ---
    call random_seed()
    call random_number(K)
    
    ! Initial Rank estimate
    initial_rank = calculate_rank_estimate(K)
    max_rank = initial_rank
    
    do t = 1, steps
        ! 1. Gaussian Blur (simplified 3x3 box blur)
        K_next = K
        do i = 2, size-1
            do j = 2, size-1
                K_next(i,j) = (K(i-1,j) + K(i+1,j) + K(i,j-1) + K(i,j+1) + K(i,j)*4.0) / 8.0
            end do
        end do
        
        ! 2. Nonlinearity
        K_next = exp(K_next * 2.0)
        K_next = K_next / maxval(K_next)
        
        ! 3. Noise
        call random_number(K) 
        K = K_next + (K - 0.5) * noise_lvl
        where (K < 0.0) K = 0.0
        where (K > 1.0) K = 1.0
        
        ! Track rank
        final_rank = calculate_rank_estimate(K)
        if (final_rank > max_rank) max_rank = final_rank
    end do
    
    rank_jump = max_rank - initial_rank
    
    ! --- JSON Output ---
    open(10, file='Step3/simulation_results_fortran.json', status='replace')
    write(10, '(A)') '{'
    write(10, '(A,F10.6,A)') '    "initial_rank": ', initial_rank, ','
    write(10, '(A,F10.6,A)') '    "final_rank": ', final_rank, ','
    write(10, '(A,F10.6,A)') '    "max_rank": ', max_rank, ','
    write(10, '(A,F10.6)')   '    "rank_jump": ', rank_jump
    write(10, '(A)') '}'
    close(10)

contains

    function calculate_rank_estimate(mat) result(r)
        real, dimension(size, size), intent(in) :: mat
        real :: r
        r = sum(mat**2) / (maxval(mat)**2 + 1e-9)
    end function calculate_rank_estimate

end program step3_vpcm_physics
